# -*- coding: utf-8 -*-
# Copyright (c) 2004-2024 Alterra, Wageningen-UR
# Allard de Wit (allard.dewit@wur.nl) and Herman Berghuijs (herman.berghuijs@wur.nl), January 2024
"""This module wraps the soil components for water and nutrients so that they run jointly
within the same model.
"""
from pcse.base import SimulationObject
from .classic_waterbalance import WaterbalanceFD, WaterbalancePP
from .watfdgw import WaterBalanceLayered, WaterBalanceLayered_PP
from .n_soil_dynamics import N_Soil_Dynamics, N_PotentialProduction
from .SNOMIN import SNOMIN
from ..traitlets import Instance
from ..decorators import prepare_states


class SoilModuleWrapper_PP(SimulationObject):
    """This wraps the soil water balance and soil N balance for potential production.
    """
    WaterbalancePP = Instance(SimulationObject)
    N_PotentialProduction = Instance(SimulationObject)

    def initialize(self, day, kiosk, parvalues):
        """
        :param day: start date of the simulation
        :param kiosk: variable kiosk of this PCSE instance
        :param parvalues: dictionary with parameter key/value pairs
        """
        self.WaterbalancePP = WaterbalancePP(day, kiosk, parvalues)
        self.N_PotentialProduction = N_PotentialProduction(day, kiosk, parvalues)

    def calc_rates(self, day, drv):
        self.WaterbalancePP.calc_rates(day, drv)
        self.N_PotentialProduction.calc_rates(day, drv)

    def integrate(self, day, delt=1.0):
        self.WaterbalancePP.integrate(day, delt)
        self.N_PotentialProduction.integrate(day, delt)


class SoilModuleWrapper_WLP_FD(SimulationObject):
    """This wraps the soil water balance for free drainage conditions and N balance
    for production conditions limited by soil water only.
    """
    WaterbalanceFD = Instance(SimulationObject)
    N_Soil_Dynamics = Instance(SimulationObject)

    def initialize(self, day, kiosk, parvalues):
        """
        :param day: start date of the simulation
        :param kiosk: variable kiosk of this PCSE instance
        :param parvalues: dictionary with parameter key/value pairs
        """
        self.WaterbalanceFD = WaterbalanceFD(day, kiosk, parvalues)
        self.N_Soil_Dynamics = N_PotentialProduction(day, kiosk, parvalues)

    def calc_rates(self, day, drv):
        self.WaterbalanceFD.calc_rates(day, drv)
        self.N_Soil_Dynamics.calc_rates(day, drv)

    def integrate(self, day, delt=1.0):
        self.WaterbalanceFD.integrate(day, delt)
        self.N_Soil_Dynamics.integrate(day, delt)


class SoilModuleWrapper_N_WLP_FD(SimulationObject):
    """This wraps the soil water balance for free drainage conditions and N balance
    for production conditions limited by both soil water and N.
    """
    WaterbalanceFD = Instance(SimulationObject)
    N_Soil_Dynamics = Instance(SimulationObject)

    def initialize(self, day, kiosk, parvalues):
        """
        :param day: start date of the simulation
        :param kiosk: variable kiosk of this PCSE instance
        :param parvalues: dictionary with parameter key/value pairs
        """
        self.WaterbalanceFD = WaterbalanceFD(day, kiosk, parvalues)
        self.N_Soil_Dynamics = N_Soil_Dynamics(day, kiosk, parvalues)

    def calc_rates(self, day, drv):
        self.WaterbalanceFD.calc_rates(day, drv)
        self.N_Soil_Dynamics.calc_rates(day, drv)

    def integrate(self, day, delt=1.0):
        self.WaterbalanceFD.integrate(day, delt)
        self.N_Soil_Dynamics.integrate(day, delt)


class SoilModuleWrapper_N(SimulationObject):
    """This wraps the soil water balance for free drainage conditions and N balance
    for production conditions limited by both soil water and N.
    """
    WaterbalancePP = Instance(SimulationObject)
    N_Soil_Dynamics = Instance(SimulationObject)

    def initialize(self, day, kiosk, parvalues):
        """
        :param day: start date of the simulation
        :param kiosk: variable kiosk of this PCSE instance
        :param parvalues: dictionary with parameter key/value pairs
        """
        self.WaterbalancePP = WaterbalancePP(day, kiosk, parvalues)
        self.N_Soil_Dynamics = N_Soil_Dynamics(day, kiosk, parvalues)

    def calc_rates(self, day, drv):
        self.WaterbalancePP.calc_rates(day, drv)
        self.N_Soil_Dynamics.calc_rates(day, drv)

    def integrate(self, day, delt=1.0):
        self.WaterbalancePP.integrate(day, delt)
        self.N_Soil_Dynamics.integrate(day, delt)

class SoilModuleWrapper_PP_multilayer(SimulationObject):
    """This wraps the soil water balance for free drainage conditions and N balance
    for production conditions limited by both soil water and N.
    """
    WaterbalanceFD = Instance(SimulationObject)
    N_Soil_Dynamics = Instance(SimulationObject)

    def initialize(self, day, kiosk, parvalues):
        """
        :param day: start date of the simulation
        :param kiosk: variable kiosk of this PCSE instance
        :param parvalues: dictionary with parameter key/value pairs
        """
        self.WaterbalanceFD = WaterBalanceLayered_PP(day, kiosk, parvalues)
        self.N_Soil_Dynamics = N_PotentialProduction(day, kiosk, parvalues)

    def calc_rates(self, day, drv):
        self.WaterbalanceFD.calc_rates(day, drv)
        self.N_Soil_Dynamics.calc_rates(day, drv)

    def integrate(self, day, delt=1.0):
        self.WaterbalanceFD.integrate(day, delt)
        self.N_Soil_Dynamics.integrate(day, delt)

class SoilModuleWrapper_WLP_FD_multilayer(SimulationObject):
    """This wraps the soil water balance for free drainage conditions and N balance
    for production conditions limited by both soil water and N.
    """
    WaterbalanceFD = Instance(SimulationObject)
    N_Soil_Dynamics = Instance(SimulationObject)

    def initialize(self, day, kiosk, parvalues):
        """
        :param day: start date of the simulation
        :param kiosk: variable kiosk of this PCSE instance
        :param parvalues: dictionary with parameter key/value pairs
        """
        self.WaterbalanceFD = WaterBalanceLayered(day, kiosk, parvalues)
        self.N_Soil_Dynamics = N_PotentialProduction(day, kiosk, parvalues)

    def calc_rates(self, day, drv):
        self.WaterbalanceFD.calc_rates(day, drv)
        self.N_Soil_Dynamics.calc_rates(day, drv)

    def integrate(self, day, delt=1.0):
        self.WaterbalanceFD.integrate(day, delt)
        self.N_Soil_Dynamics.integrate(day, delt)

class SoilModuleWrapper_NLP_FD_multilayer(SimulationObject):
    """This wraps the soil water balance for free drainage conditions and N balance
    for production conditions limited by both soil water and N.
    """
    WaterbalanceFD = Instance(SimulationObject)
    N_Soil_Dynamics = Instance(SimulationObject)

    def initialize(self, day, kiosk, parvalues):
        """
        :param day: start date of the simulation
        :param kiosk: variable kiosk of this PCSE instance
        :param parvalues: dictionary with parameter key/value pairs
        """
        self.WaterbalanceFD = WaterBalanceLayered_PP(day, kiosk, parvalues)
        self.N_Soil_Dynamics = N_Soil_Dynamics(day, kiosk, parvalues)

    def calc_rates(self, day, drv):
        self.WaterbalanceFD.calc_rates(day, drv)
        self.N_Soil_Dynamics.calc_rates(day, drv)

    def integrate(self, day, delt=1.0):
        self.WaterbalanceFD.integrate(day, delt)
        self.N_Soil_Dynamics.integrate(day, delt)

class SoilModuleWrapper_NWLP_FD_multilayer(SimulationObject):
    """This wraps the soil water balance for free drainage conditions and N balance
    for production conditions limited by both soil water and N.
    """
    WaterbalanceFD = Instance(SimulationObject)
    N_Soil_Dynamics = Instance(SimulationObject)

    def initialize(self, day, kiosk, parvalues):
        """
        :param day: start date of the simulation
        :param kiosk: variable kiosk of this PCSE instance
        :param parvalues: dictionary with parameter key/value pairs
        """
        self.WaterbalanceFD = WaterBalanceLayered(day, kiosk, parvalues)
        self.N_Soil_Dynamics = N_Soil_Dynamics(day, kiosk, parvalues)

    def calc_rates(self, day, drv):
        self.WaterbalanceFD.calc_rates(day, drv)
        self.N_Soil_Dynamics.calc_rates(day, drv)

    def integrate(self, day, delt=1.0):
        self.WaterbalanceFD.integrate(day, delt)
        self.N_Soil_Dynamics.integrate(day, delt)

class SoilModuleWrapper_SNOMIN(SimulationObject):
    """This wraps the soil water balance for free drainage conditions and N balance
    for production conditions limited by both soil water and N.
    """
    WaterbalanceFD = Instance(SimulationObject)
    N_Soil_Dynamics = Instance(SimulationObject)

    def initialize(self, day, kiosk, parvalues):
        """
        :param day: start date of the simulation
        :param kiosk: variable kiosk of this PCSE instance
        :param parvalues: dictionary with parameter key/value pairs
        """
        self.WaterbalanceFD = WaterBalanceLayered(day, kiosk, parvalues)
        self.N_Soil_Dynamics = SNOMIN(day, kiosk, parvalues)

    def calc_rates(self, day, drv):
        self.WaterbalanceFD.calc_rates(day, drv)
        self.N_Soil_Dynamics.calc_rates(day, drv)

    def integrate(self, day, delt=1.0):
        self.WaterbalanceFD.integrate(day, delt)
        self.N_Soil_Dynamics.integrate(day, delt)