import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

"""
define parameters 
"""
T=300 #temperature
tox=10e-9*100# define thickness of oxide 50nm
Nd=1e17 #donor doping concentration N/cm^3
Na=1e15# acceptor doping concentration N/cm^3
CBO=3.85# conduction band off set eV
VBO=4.4 # SiO2/GaAs valence band offset, eV
"""
Physical constant
"""
e0=8.854e-14 #permittivity of free space F/cm
q=1.602e-19 #elementary charge, Coulombs
k=8.617e-5 #Bontzmann constant, eV/K


"""
Material parameter
"""
es=12.88 #relative permittivity, GaAs
eox=3.9 #ralative permittivity, SiO2
chi_s=4.07 #electron effinity, GaAs, eV
phi_m=5.03 #work function, Gold, eV

#bandgap GaAs, eV
Eg=1.519 - 5.408e-4*T**2/(T+204.0) # 1.519 - 5.408 ⋅ 10-4 T2/( T + 204)
Nv=3.5e15*T**1.5 # effective valence band DOS number/cm^3
Nc=6.215*T**1.5 #effective conduction band DOS number/cm^3

def bisection(func, target, xmin, xmax):
    error=1e-19
    max_iters = 1e2 # maximum number of iterations
    a = xmin
    b = xmax
    cnt = 1
    Fa = target - func(a)
    c = a

    # bisection search loop (referene: H-Gens)
    while np.abs(a - b) > error and cnt < max_iters:
        cnt += 1
        # 'c' be the midpoint between 'a' and 'b' for two material
        c = (a + b) / 2.0
        # calculate at the new 'c'
        Fc = target - func(c)

        if Fc == 0:
            # 'c' was the sought-after solution, so quit
            break
        elif np.sign(Fa) == np.sign(Fc):
            # the signs were the same, so modify 'a'
            a = c
            Fa = Fc
        else:
            # the signs were different, so modify 'b'
            b = c

    if cnt == max_iters:
        print('WARNING: max iterations reached')

    return c 
"""
dependent variable calculation
"""
ni = np.sqrt(Nc * Nv) * np.exp(-Eg / (2 * k * T)) #intrinsic carrier concentration
Ev = 0 # valence band energy level
Ec = Eg # conduction band energy level
Ei = k * T * np.log(ni / Nc) + Ec
phit = k * T # thermal voltage, eV
n = lambda Ef: Nc * np.exp((-Ec + Ef) / phit)
p = lambda Ef: Nv * np.exp((Ev - Ef) / phit)
func = lambda Ef: p(Ef) - n(Ef) + Nd - Na
Ef = bisection(func, 0, Ev, Ec)
phi_s = chi_s + Ec - Ef
phi_ms = phi_m - phi_s # metal-semiconductor workfunction, eV
Vfb = phi_ms # flatband voltage, V
Coxp = eox * e0 / tox
if Na > Nd:
    Na = Na - Nd
    Nd = 0
    device_type = 'ntype'
else:
    Nd = Nd - Na
    Na = 0
    device_type = 'ptype'

# define the SPE
# -----------------------
# compute equilibrium carrier concentrations
n_o = Nc * np.exp((-Ec + Ef) / phit)
p_o = Nv * np.exp((Ev - Ef) / phit)
# define the charge function so it can be used in the SPE
f = lambda psis: psis * (Na - Nd) \
  + phit * p_o * (np.exp(-psis / phit) - 1) \
  + phit * n_o * (np.exp(psis / phit) - 1)
Qs = lambda psis: -np.sign(psis) * np.sqrt(2 * q * e0 * es * f(psis))
SPE = lambda psis: Vfb + psis - Qs(psis) / Coxp
# define the electric field for use in computing y(psi)
E = lambda psi: np.sign(psi) * np.sqrt(2 * q / (es * e0) * f(psi))
integrand_y = lambda psi: 1 / E(psi)

def compute_y_vs_psi(psis):
    """
    This function creates a 'psi' variable ranging from psis to ~zero.
    It then computes the y-values corresponding to every value in psi.

    psis is the surface potential and must be a scalar constant.
    """
    # handle the flatband case
    if psis == 0:
        y = np.linspace(0, 200, 101) * 1e-7 # convert nm to cm
        psi = 0 * y
        return y, psi
    # (1) let semiconductor potential range from psis to near-zero
    # - could construct psi linearly and have a coarse y as psi -> 0
    # - could construct psi log-spaced to make y more evenly spaced
    # - solution: do a mixture 
    psi1 = np.linspace(psis, psis * 0.5, 21) # linear spacing near y=0
    psi2 = np.logspace(                      # log spacing toward bulk
        np.log10(np.abs(psis * 0.5)), 
        np.log10(np.abs(psis * 1e-3)), 
        101
    )
    if psis < 0:
        psi2 = -1 * psi2
    # combine the arrays, but leave out the common point (psis * 0.5)
    psi = np.hstack((psi1, psi2[1:]))
    # (2) call compute_y() at every value in psi
    # collect the returned y-values in an array
    y = np.array([])
    for value in psi:
        y_current, error = quad(integrand_y, value, psis)
        y = np.hstack((y, y_current))
    return y, psi


# -----------------------
# choose a potential to plot
# -----------------------
# psis = Ev - Ef                    # (very) strong accumulation
# psis = 0                          # flatband
# psis = Ei - Ef                    # weak inversion
# psis = 2 * (Ei - Ef)              # strong inversion
# psis = 2 * (Ei - Ef) + 3 * phit   # stronger inversion
# psis = Ec - Ef                    # (very) strong inversion
psis = bisection(           # zero gate-bulk bias
    SPE, 0, Ev - Ef, Ec - Ef
)

# compute the corresponding Vgb value
Vgb = SPE(psis)

# create figure, label axes, turn grid on
plt.figure(1)
plt.xlabel('y (nm)', fontsize=14)
plt.ylabel('relative to bulk valence band (eV)', fontsize=14)
plt.grid(True)

# get psiox from the potential balance equation (see SPE derivation)
psiox = Vgb - psis - phi_ms

# construct the psi vs y curve
y, psi = compute_y_vs_psi(psis)
# y and tox are in cm, so convert to nm
y = y / 100 * 1e9
toxnm = tox / 100 * 1e9

# plot the conduction/intrinsic/valence bands
plt.plot(y, Ev - psi, 'b')
plt.plot(y, Ei - psi, 'b--')
plt.plot(y, Ec - psi, 'b')

# plot the fermi level
plt.plot(y, 0 * y + Ef, 'k')

# plot the SiO2 bands
plt.plot([0, 0], [Ev - psis - VBO, Ec - psis + CBO], 'r')
plt.plot(
    [-toxnm, -toxnm], 
    [Ev - psis - VBO - psiox, Ec - psis + CBO - psiox], 
    'r'
)
plt.plot([-toxnm, 0], [Ev - psis - VBO - psiox, Ev - psis - VBO], 'r')
plt.plot([-toxnm, 0], [Ec - psis + CBO - psiox, Ec - psis + CBO], 'r')

# plot the gate's Fermi level
plt.plot(
    [-toxnm - 15, -toxnm], 
    [Ef - phi_ms - psis - psiox, Ef - phi_ms - psis - psiox],
    'k'
)

print('Vgb = %0.4g, psiox = %0.4g, psis = %0.4g' % (Vgb, psiox, psis))

plt.show()