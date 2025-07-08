"""

1. Importing all functions from packages
2. Creating one dictionary "function_tree" that is used in "functions_calculator.py"

"""

from petrocalc.PVT.interfacial_tension import (
    iftgo_abdul_majeed,
    iftgo_baker_swerdloff,
)
from petrocalc.PVT.pvt_gas import (
    zfactor_brill_beggs,
    zfactor_dak,
    ppc_standing,
    tpc_standing,
    ppc_sutton,
    tpc_sutton,
    bg,
    ug_lge,
    cg,
    gas_density,
)
# ───────────────────────────────────────────────────────────────────────
#  Oil-, gas-, water-PVT
# ───────────────────────────────────────────────────────────────────────
from petrocalc.PVT.pvt_oil import (
    pbo_al_marhoun,
    pbo_dokla_osman,
    pbo_petrosky_farshad,
    pbo_vasquez_beggs,
    pbo_dindoruk_christman,
    pbo_glaso,
    pbo_standing,
    bo_sat_al_marhoun_1988,
    bo_sat_glaso_1980,
    bo_sat_standing_1947,
    bo_u_sat,
    bo_sat_dindoruk_christman_2001,
    bo_sat_petrosky_1990,
    bo_sat_vasquez_beggs_1980,
    rso_al_marhoun_1988,
    rso_glaso_1980,
    rso_standing_1981,
    rso_dindoruk_christman_2001,
    rso_petrosky_farshad_1993,
    rso_vasquez_beggs_1980,
    uod_egbogah_1983,
    uo_usat_vasquez_beggs_1980,
    uo_sat_beggs_robinson_1975,
    co_sat_villena_lanzi_1985,
    co_usat_vasquez_beggs_1980,
)
from petrocalc.PVT.pvt_water import (
    bw_mc_cain,
    rsw_mc_cain,
    rswp_mc_cain,
    cw_sat_mc_cain,
    cw_usat_osif,
    uw_mc_cain,
    uw1_mc_cain,
)
from petrocalc.decline_curve_analysis.decline_curves import (
    exponential_decline_rate,
    exponential_decline_cumulative,
    harmonic_decline_rate,
    harmonic_decline_cumulative,
    hyperbolic_decline_rate,
    hyperbolic_decline_cumulative,
    modified_hyperbolic_decline_rate,
    modified_hyperbolic_decline_cumulative,
    ple_decline_rate,
)
from petrocalc.decline_curve_analysis.production_profiles import (
    basic_field_profile,
    combined_field_profile,
)
from petrocalc.pipe_flow.multiphase_pipe_flow import (
    pressure_gradient_har_brown,
    inlet_pressure_har_brown,
    outlet_pressure_har_brown,
    pressure_gradient_beggs_brill,
    inlet_pressure_beggs_brill,
    outlet_pressure_beggs_brill,
    pressure_gradient_gray,
    inlet_pressure_gray,
    outlet_pressure_gray,
)
# ───────────────────────────────────────────────────────────────────────
#  Pipe-flow correlations
# ───────────────────────────────────────────────────────────────────────
from petrocalc.pipe_flow.single_phase_fluid_flow import (
    reynolds_number_liquid,
    friction_pressure_drop_liquid,
    outlet_pipe_pressure_liquid,
    inlet_pipe_pressure_liquid,
    potential_energy_pressure_drop_liquid,
    reynolds_number_gas,
    inlet_pipe_pressure_gas,
    outlet_pipe_pressure_gas,
)
from petrocalc.pressure_transient_analysis.dimensionless import (
    pta_cd,
    pta_ld,
    pta_pd,
    pta_rwd,
    pta_td,
)
from petrocalc.pressure_transient_analysis.pta_dimensionless_models import (
    pd_lssihr,
    pdw_vwihr,
    pdw_vwihrlcpb,
    pdw_vwihrlsfb,
    pdw_vwihrpcpb,
    pdw_vwihrpmb,
    pdw_vwihrpsfb
)
# ───────────────────────────────────────────────────────────────────────
#  Pressure-transient analysis
# ───────────────────────────────────────────────────────────────────────
from petrocalc.pressure_transient_analysis.pta_models import (
    pw_vwihr,
    pw_vwihrlcpb,
    pw_vwihrlsfb,
    pw_vwihrpcpb,
    pw_vwihrpmb,
    pw_vwihrpsfb,
)
# ───────────────────────────────────────────────────────────────────────
#  Special-core analysis
# ───────────────────────────────────────────────────────────────────────
from petrocalc.special_core_analysis.relative_permeability_models import (
    krow_corey,
    krw_corey,
    krow_let,
    krw_let,
    krow_honarpour_carb_inter_wet,
    krow_honarpour_sand_inter_wet,
    krw_honarpour_carb_inter_wet,
    krw_honarpour_sand_inter_wet,
    krow_honarpour_carb_water_wet,
    krow_honarpour_sand_water_wet,
    krw_honarpour_carb_water_wet,
    krw_honarpour_sand_water_wet,
    krcgl_k_gas_cond,
    krgl_k_gas_cond,
    krgl_k_gas_oil_carb,
    krgl_k_gas_oil_sand,
    krgw_ik_gas_water,
    krog_ik_gas_oil_carb,
    krog_ik_gas_oil_sand,
    krowl_k_carb_oil_wet,
    krowl_k_carb_water_wet,
    krowl_k_carb_inter_wet,
    krowl_k_carb_strong_water_wet,
    krowl_k_sand_oil_wet,
    krowl_k_sand_water_wet,
    krowl_k_sand_inter_wet,
    krowl_k_sand_strong_water_wet,
    krwl_k_carb_oil_wet,
    krwl_k_carb_water_wet,
    krwl_k_carb_inter_wet,
    krwl_k_carb_strong_water_wet,
    krwl_k_gas_water,
    krwl_k_sand_oil_wet,
    krwl_k_sand_water_wet,
    krwl_k_sand_inter_wet,
    krwl_k_sand_strong_water_wet,
)
from petrocalc.special_core_analysis.rock_compressibility import (
    cf_newman_l,
    cf_newman_s,
)
from petrocalc.utilities.conversion import api_2sg, sg_2api, unit_converter
# ───────────────────────────────────────────────────────────────────────
#  Utilities
# ───────────────────────────────────────────────────────────────────────
from petrocalc.utilities.interpolation import (
    cubic_spline_differentiate,
    cubic_spline_integrate,
    cubic_spline_integrate_t1_t2,
    cubic_spline_interpolate,
    cubic_splines_intersection,
    data_differentiate,
    linear_spline_differentiate,
    linear_spline_integrate,
    linear_spline_integrate_t1_t2,
    linear_spline_interpolate,
    linear_splines_intersection,
    step_interpolate,
    proximal_interpolate,
)
from petrocalc.utilities.special_functions import exp_integral_ei
from petrocalc.well_flow_perfomance.gas_well_production import (
    gas_flow_rate_pss,
    gas_flow_rate_pss_non_darcy,
    non_darcy_coefficient,
    time_to_pss_gas,
)
# ───────────────────────────────────────────────────────────────────────
#  Misc geometry helpers
# ───────────────────────────────────────────────────────────────────────
from petrocalc.well_flow_perfomance.miscellaneous import (
    drainage_area_hor_well_1,
    drainage_area_hor_well_2,
    drainage_radius,
    effective_wellbore_radius,
    equivalent_skin_factor,
)
# ───────────────────────────────────────────────────────────────────────
#  Well-flow performance
# ───────────────────────────────────────────────────────────────────────
from petrocalc.well_flow_perfomance.oil_well_production import (
    flow_rate_pss,
    flow_rate_pss_vogel,
    prod_index_hor_well_bo,
    prod_index_hor_well_bo2,
    prod_index_pss,
    time_to_pss,
    flow_rate_ss,
    flow_rate_ss_vogel,
    prod_index_hor_well_borisov,
    prod_index_hor_well_grj,
    prod_index_hor_well_joshi,
    prod_index_hor_well_rd,
    prod_index_ss,
    flow_rate_tf,
    flow_rate_tf_vogel,
    prod_index_tf,
)

# ───────────────────────────────────────────────────────────────────────
#  Дерево навигации (скопировано из вашего исходного файла)
# ───────────────────────────────────────────────────────────────────────
function_tree = {
    "Decline Curve Analysis": {
        "Decline Curves": {
            "Exponential": {
                "Rate": exponential_decline_rate,
                "Cumulative": exponential_decline_cumulative,
            },
            "Harmonic": {
                "Rate": harmonic_decline_rate,
                "Cumulative": harmonic_decline_cumulative,
            },
            "Hyperbolic": {
                "Rate": hyperbolic_decline_rate,
                "Cumulative": hyperbolic_decline_cumulative,
            },
            "Modified Hyperbolic": {
                "Rate": modified_hyperbolic_decline_rate,
                "Cumulative": modified_hyperbolic_decline_cumulative,
            },
            "PLE": {
                "Rate": ple_decline_rate,
            },
        },
        "Production Profiles": {
            "Basic Field Profile": basic_field_profile,
            "Combined Field Profile": combined_field_profile,
        },
    },
    "PVT": {
        "Oil PVT": {
            "Oil Bubble Point Pressure": {
                "Pbo AI Marhoun": pbo_al_marhoun,
                "Pbo Dokla Osman": pbo_dokla_osman,
                "Pbo Petrosky Farshad": pbo_petrosky_farshad,
                "Pbo Vasquez Beggs": pbo_vasquez_beggs,
                "Pbo Dindoruk Christman": pbo_dindoruk_christman,
                "Pbo Glaso": pbo_glaso,
                "Pbo Standing": pbo_standing,
            },
            "Oil Formation Volume Factor": {
                "Bo Sat Al Marhoun 1988": bo_sat_al_marhoun_1988,
                "Bo Sat Glaso 1980": bo_sat_glaso_1980,
                "Bo Sat Standing 1988": bo_sat_standing_1947,
                "Bo U Sat": bo_u_sat,
                "Bo Sat Dindoruk Christman 2001": bo_sat_dindoruk_christman_2001,
                "Bo Sat Petrosky 1990": bo_sat_petrosky_1990,
                "Bo Sat Vasquez Beggs 1980": bo_sat_vasquez_beggs_1980,
            },
            "Solution Gas-Oil Ratio": {
                "Rso Al Marhoun 1988": rso_al_marhoun_1988,
                "Rso Glaso 1980": rso_glaso_1980,
                "Rso Standing 1981": rso_standing_1981,
                "Rso Dindoruk Christman 2001": rso_dindoruk_christman_2001,
                "Rso Petrosky Farshad 1993": rso_petrosky_farshad_1993,
                "Rso Vasquez Beggs 1980": rso_vasquez_beggs_1980,
            },
            "Oil Viscosity": {
                "Uod Egbogah 1983": uod_egbogah_1983,
                "Uo USat Vasquez Beggs 1980": uo_usat_vasquez_beggs_1980,
                "Uo Sat Beggs Robinson 1975": uo_sat_beggs_robinson_1975,
            },
            "Oil Compressibility": {
                "Co Sat Villena Lanzi 1985": co_sat_villena_lanzi_1985,
                "Co USat Vasquez Beggs 1980": co_usat_vasquez_beggs_1980,
            },
        },
        "Gas PVT": {
            "Z Factor": {
                "Zfactor Brill Beggs": zfactor_brill_beggs,
                "Zfactor Dak": zfactor_dak,
            },
            "Pseudo Critical P and T": {
                "Ppc Standing": ppc_standing,
                "Tpc Standing": tpc_standing,
                "Ppc Sutton": ppc_sutton,
                "Tpc Sutton": tpc_sutton,
            },
            "Gas Formation Volume Factor": {"Bg": bg},
            "Gas Viscosity": {"Ug LGE": ug_lge},
            "Gas Compressibility": {"Cg": cg},
            "Gas Density": {"Gas density": gas_density},
        },
        "Water PVT": {
            "Water Formation Volume Factor": {"Bw Mc Cain": bw_mc_cain},
            "Solution Gas-Water Ratio": {
                "Rsw Mc Cain": rsw_mc_cain,
                "Rswp Mc Cain": rswp_mc_cain,
            },
            "Water Compressibility": {
                "Cw Sat Mc Cain": cw_sat_mc_cain,
                "Cw USat Osif": cw_usat_osif,
            },
            "Water Viscosity": {
                "Uw Mc Cain": uw_mc_cain,
                "Uw1 Mc Cain": uw1_mc_cain,
            },
        },
        "Interfacial Tension": {
            "IFTgo Abdul Majeed": iftgo_abdul_majeed,
            "IFTgo Baker Swerdloff": iftgo_baker_swerdloff,
        },
    },
    "Pipe Flow": {
        "Single-Phase Fluid Flow": {
            "Liquid Pipe Flow": {
                "Friction Pressure Drop Liquid": friction_pressure_drop_liquid,
                "Outlet Pipe Pressure Liquid": outlet_pipe_pressure_liquid,
                "Reynolds Number Liquid": reynolds_number_liquid,
                "Inlet Pipe Pressure Liquid": inlet_pipe_pressure_liquid,
                "Potential Energy Drop Pressure Liquid": potential_energy_pressure_drop_liquid,
            },
            "Gas Pipe Flow": {
                "Inlet Pipe Pressure Gas": inlet_pipe_pressure_gas,
                "Reynolds Number Gas": reynolds_number_gas,
                "Outlet Pipe Pressure Gas": outlet_pipe_pressure_gas,
            },
        },
        "Multiphase Pipe Flow": {
            "Hagedorn and Brown Correlation": {
                "Inlet Pressure Har Brown": inlet_pressure_har_brown,
                "Outlet Pressure Har Brown": outlet_pressure_har_brown,
                "Pressure Gradient Har Brown": pressure_gradient_har_brown,
            },
            "Beggs and Brill Correlation": {
                "Inlet Pressure Beggs Brill": inlet_pressure_beggs_brill,
                "Outlet Pressure Beggs Brill": outlet_pressure_beggs_brill,
                "Pressure Gradient Beggs Brill": pressure_gradient_beggs_brill,
            },
            "Gray Correlation": {
                "Inlet Pressure Gray": inlet_pressure_gray,
                "Outlet Pressure Gray": outlet_pressure_gray,
                "Pressure Gradient Gray": pressure_gradient_gray,
            },
        },
    },
    "Well Flow Performance": {
        "Oil Well Production": {
            "Oil Pseudo-steady State Flow": {
                "Flow Rate PSS": flow_rate_pss,
                "Flow Rate PSS Vogel": flow_rate_pss_vogel,
                "Prod Index Hor Well BO": prod_index_hor_well_bo,
                "Prod Index Hor Well BO2": prod_index_hor_well_bo2,
                "Prod Index PSS": prod_index_pss,
                "Time To PSS": time_to_pss,
            },
            "Oil Steady State Flow": {
                "Flow Rate SS": flow_rate_ss,
                "Flow Rate SS Vogel": flow_rate_ss_vogel,
                "Prod Index Hor Well Borisov": prod_index_hor_well_borisov,
                "Prod Index Hor Well GRJ": prod_index_hor_well_grj,
                "Prod Index Hor Well Joshi": prod_index_hor_well_joshi,
                "Prod Index Hor Well RD": prod_index_hor_well_rd,
                "Prod Index SS": prod_index_ss,
            },
            "Oil Transient Flow": {
                "Flow Rate TF": flow_rate_tf,
                "Flow Rate TF Vogel": flow_rate_tf_vogel,
                "Prod Index TF": prod_index_tf,
            },
        },
        "Gas Well Production": {
            "Gas Pseudo-steady State Flow": {
                "Gas Flow Rate PSS": gas_flow_rate_pss,
                "Gas Flow Rate PSS Non Darcy": gas_flow_rate_pss_non_darcy,
                "Non Darcy Coefficient": non_darcy_coefficient,
                "Time To PSS Gas": time_to_pss_gas,
            }
        },
        "Miscellaneous": {
            "Drainage Geometry": {
                "Drainage Area Hor Well 1": drainage_area_hor_well_1,
                "Drainage Area Hor Well 2": drainage_area_hor_well_2,
                "Drainage Radius": drainage_radius,
                "Effective Wellbore Radius": effective_wellbore_radius,
                "Equivalent Skin Factor": equivalent_skin_factor,
            },
        },
    },
    "Pressure Transient Analysis": {
        "PTA Models": {
            "Pw VWIHR": pw_vwihr,
            "Pw VWIHRLCPB": pw_vwihrlcpb,
            "Pw VWIHRLSFB": pw_vwihrlsfb,
            "Pw VWIHRPCPB": pw_vwihrpcpb,
            "Pw VWIHRPMB": pw_vwihrpmb,
            "Pw VWIHRPSFB": pw_vwihrpsfb,
        },
        "PTA Dimensionless Models": {
            "Pd LSSIHR": pd_lssihr,
            "Pdw VWIHR": pdw_vwihr,
            "Pdw VWIHRLCPB": pdw_vwihrlcpb,
            "Pdw VWIHRLSFB": pdw_vwihrlsfb,
            "Pdw VWIHRPCPB": pdw_vwihrpcpb,
            "Pdw VWIHRPMB": pdw_vwihrpmb,
            "Pdw VWIHRPSFB": pdw_vwihrpsfb,
        },
        "Dimensionless": {
            "pta Cd": pta_cd,
            "pta Ld": pta_ld,
            "pta Pd": pta_pd,
            "pta Rwd": pta_rwd,
            "pta Td": pta_td,
        },
    },
    "Special Core Analysis": {
        "Relative Permeability Models": {
            "Corey Correlation": {
                "Krow Corey": krow_corey,
                "Krw Corey": krw_corey,
            },
            "LET Correlation": {
                "Krow LET": krow_let,
                "Krw LET": krw_let,
            },
            "Honarpur Correlation": {
                "Krow Honarpour Carb InterWet": krow_honarpour_carb_inter_wet,
                "Krow Honarpour Sand InterWet": krow_honarpour_sand_inter_wet,
                "Krw Honarpour Carb InterWet": krw_honarpour_carb_inter_wet,
                "Krw Honarpour Sand InterWet": krw_honarpour_sand_inter_wet,
                "Krow Honarpour Carb WaterWet": krow_honarpour_carb_water_wet,
                "Krow Honarpour Sand WaterWet": krow_honarpour_sand_water_wet,
                "Krw Honarpour Carb WaterWet": krw_honarpour_carb_water_wet,
                "Krw Honarpour Sand WaterWet": krw_honarpour_sand_water_wet,
            },
            "Ibrahim-Koederitz Correlation": {
                "Krcgl KGasCond": krcgl_k_gas_cond,
                "Krgl KGasCond": krgl_k_gas_cond,
                "Krgl KGasOilCarb": krgl_k_gas_oil_carb,
                "Krgl KGasOilSand": krgl_k_gas_oil_sand,
                "Krgw IKGasWater": krgw_ik_gas_water,
                "Krogl KGasOilCarb": krog_ik_gas_oil_carb,
                "Krogl KGasOilSand": krog_ik_gas_oil_sand,
                "Krowl KCarbOilWet": krowl_k_carb_oil_wet,
                "Krowl KCarbWaterWet": krowl_k_carb_water_wet,
                "Krowl KCarbInterWet": krowl_k_carb_inter_wet,
                "Krowl KCarbStrongWaterWet": krowl_k_carb_strong_water_wet,
                "Krowl KSandOilWet": krowl_k_sand_oil_wet,
                "Krowl KSandWaterWet": krowl_k_sand_water_wet,
                "Krowl KSandInterWet": krowl_k_sand_inter_wet,
                "Krowl KSandStrongWaterWet": krowl_k_sand_strong_water_wet,
                "Krw IKCarbOilWet": krwl_k_carb_oil_wet,
                "Krw IKCarbWaterWet": krwl_k_carb_water_wet,
                "Krw IKCarbInterWet": krwl_k_carb_inter_wet,
                "Krw IKCarbStrongWaterWet": krwl_k_carb_strong_water_wet,
                "Krw IKGasWater": krwl_k_gas_water,
                "Krw IKSandOilWet": krwl_k_sand_oil_wet,
                "Krw IKSandWaterWet": krwl_k_sand_water_wet,
                "Krw IKSandInterWet": krwl_k_sand_inter_wet,
                "Krw IKSandStrongWaterWet": krwl_k_sand_strong_water_wet,
            },
        },
        "Rock Compressibility": {
            "Cf Newman L": cf_newman_l,
            "Cf Newman S": cf_newman_s,
        },
    },
    "Utilities": {
        "Interpolation": {
            "CubicSplineDifferentiate": cubic_spline_differentiate,
            "CubicSplineIntegrate": cubic_spline_integrate,
            "CubicSplineIntegrateT1T2": cubic_spline_integrate_t1_t2,
            "CubicSplineInterpolate": cubic_spline_interpolate,
            "CubicSplinesIntersection": cubic_splines_intersection,
            "DataDifferentiate": data_differentiate,
            "LinearSplineDifferentiate": linear_spline_differentiate,
            "LinearSplineIntegrate": linear_spline_integrate,
            "LinearSplineIntegrateT1T2": linear_spline_integrate_t1_t2,
            "LinearSplineInterpolate": linear_spline_interpolate,
            "LinearSplinesIntersection": linear_splines_intersection,
            "StepInterpolate": step_interpolate,
            "ProximalInterpolate": proximal_interpolate,
        },
        "Conversion": {
            "API 2SG": api_2sg,
            "SG2 API": sg_2api,
            "Unit converter": unit_converter
        },
        "Special Functions": {
            "Exp Integral Ei": exp_integral_ei,
        },
    },
}

__all__ = ["function_tree"]
