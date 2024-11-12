from cnwheat import model, parameters


class Collar:
    def calculate_Unloading_Sucrose(self, sucrose_roots, sucrose_phloem, mstruct_axis, T_effect_conductivity):
        """Rate of sucrose Unloading from phloem to roots (µmol` C sucrose unloaded g-1 mstruct h-1).

        :param float sucrose_roots: Amount of sucrose in roots (µmol` C)
        :param float sucrose_phloem: Amount of sucrose in phloem (µmol` C)
        :param float mstruct_axis: The structural dry mass of the axis (g)
        :param float T_effect_conductivity: Effect of the temperature on the conductivity rate at 20µC (AU)

        :return: Rate of Sucrose Unloading (µmol` C.h-1)
        :rtype: float
        """
        conc_sucrose_phloem_roots = max(0, sucrose_roots / (self.mstruct * self.__class__.PARAMETERS.ALPHA))
        conc_sucrose_phloem_shoot = max(0, sucrose_phloem / ((mstruct_axis - self.mstruct) * parameters.AXIS_PARAMETERS.ALPHA))
        # This initialization situation is accounted for to avoid unlogical depleating when one of the models is initialized too low

        #: Driving compartment (µmol` C g-1 mstruct)
        driving_sucrose_compartment = max(conc_sucrose_phloem_shoot, conc_sucrose_phloem_roots)
        #: Gradient of sucrose between the roots and the phloem (µmol` C g-1 mstruct)
        diff_sucrose = conc_sucrose_phloem_shoot - conc_sucrose_phloem_roots
        #: Conductance depending on mstruct (g2 µmol`-1 s-1)
        conductance = parameters.ROOTS_PARAMETERS.SIGMA_SUCROSE * parameters.ROOTS_PARAMETERS.BETA * self.mstruct ** (2 / 3) * T_effect_conductivity
        flow_value = driving_sucrose_compartment * diff_sucrose * conductance * parameters.SECOND_TO_HOUR_RATE_CONVERSION

        # minimal_phloem_concentration = 0 # mol.g-1
        # if flow_value > 0.:
        #     if (sucrose_phloem - flow_value) / (mstruct_axis - self.mstruct) < minimal_phloem_concentration:
        #         flow_value = 0.
        #         print("WARNING blocked root phloem unloading")
        
        # else:
        #     if (sucrose_roots + flow_value) / self.mstruct < minimal_phloem_concentration:
        #         flow_value = 0.
        #         print("WARNING blocked shoot phloem unloading")

        #print(conc_sucrose_phloem_shoot, conc_sucrose_phloem_roots, flow_value)

        return flow_value

    def calculate_Unloading_Sucrose_homogeneous(self, sucrose_roots, sucrose_phloem, mstruct_axis, T_effect_conductivity):
        """
        Rate of sucrose Unloading from phloem to roots (µmol` C sucrose unloaded g-1 mstruct h-1).
        We compute the flow necessary to mean the concentrations between shoot and root phloem, as they are considered as homogeneous for young cereals.
        """
        #conc_sucrose_whole_phloem = (sucrose_roots + sucrose_phloem) / (self.mstruct + mstruct_axis)
        conc_sucrose_whole_phloem = (sucrose_roots + sucrose_phloem) / (mstruct_axis)
        flow_value = (conc_sucrose_whole_phloem * self.mstruct) - sucrose_roots
        # if flow_value > 0.25*sucrose_phloem:
        #     print("low warning")
        #     if flow_value > 0.5*sucrose_phloem:
        #         print("first warning")
        #         if flow_value > 0.75*sucrose_phloem:
        #             print("second warning")
        #             if flow_value > 0.95*sucrose_phloem:
        #                 print("flow is too high compared to shoot content!")
        return flow_value
    

model.Roots.calculate_Unloading_Sucrose = Collar.calculate_Unloading_Sucrose
