from cnwheat import model, parameters


class Collar:
    def calculate_Unloading_Sucrose_homogeneous(self, sucrose_roots, sucrose_phloem, mstruct_axis, T_effect_conductivity):
        """Rate of sucrose Unloading from phloem to roots (µmol` C sucrose unloaded g-1 mstruct h-1).


        :param float sucrose_roots: Amount of sucrose in roots (µmol` C)
        :param float sucrose_phloem: Sucrose concentration in phloem (µmol` C g-1 mstruct)
        :param float mstruct_axis: The structural dry mass of the axis (g)
        :param float T_effect_conductivity: Effect of the temperature on the conductivity rate at 20µC (AU)

        :return: Rate of Sucrose Unloading from shoot homogeneous phloem to root homogeneous phloem (µmol` C g-1 mstruct h-1)
        :rtype: float
        """
        # We compute the flow necessary to mean the concentrations between shoot and root phloem, as they are considered as homogeneous.
        conc_sucrose_whole_phloem = (sucrose_roots + sucrose_phloem) / (self.mstruct + mstruct_axis)

        return max((conc_sucrose_whole_phloem * self.mstruct) - sucrose_roots, 0.)


    def calculate_Unloading_Sucrose(self, sucrose_roots, sucrose_phloem, mstruct_axis, T_effect_conductivity):
        """Rate of sucrose Unloading from phloem to roots (µmol` C sucrose unloaded g-1 mstruct h-1).

        :param float sucrose_roots: Amount of sucrose in roots (µmol` C)
        :param float sucrose_phloem: Amount of sucrose in phloem (µmol` C)
        :param float mstruct_axis: The structural dry mass of the axis (g)
        :param float T_effect_conductivity: Effect of the temperature on the conductivity rate at 20µC (AU)

        :return: Rate of Sucrose Unloading (µmol` C g-1 mstruct h-1)
        :rtype: float
        """

        conc_sucrose_phloem_roots = sucrose_roots / (self.mstruct * self.__class__.PARAMETERS.ALPHA)
        conc_sucrose_phloem_shoot = sucrose_phloem / (mstruct_axis * parameters.AXIS_PARAMETERS.ALPHA)
        # This initialization situation is accounted for to avoid unlogical depleating when one of the models is initialized too low

        if conc_sucrose_phloem_shoot == 0. or conc_sucrose_phloem_roots > conc_sucrose_phloem_shoot:
            return 0.
        else:
            #: Driving compartment (µmol` C g-1 mstruct)
            driving_sucrose_compartment = max(conc_sucrose_phloem_shoot, conc_sucrose_phloem_roots)
            #: Gradient of sucrose between the roots and the phloem (µmol` C g-1 mstruct)
            diff_sucrose = conc_sucrose_phloem_shoot - conc_sucrose_phloem_roots
            #: Conductance depending on mstruct (g2 µmol`-1 s-1)
            conductance = parameters.ROOTS_PARAMETERS.SIGMA_SUCROSE * parameters.ROOTS_PARAMETERS.BETA * self.mstruct ** (2 / 3) * T_effect_conductivity
            flow_value = driving_sucrose_compartment * diff_sucrose * conductance * parameters.SECOND_TO_HOUR_RATE_CONVERSION
            #print(sucrose_phloem, sucrose_roots, flow_value/(self.mstruct + mstruct_axis))
            return flow_value


model.Roots.calculate_Unloading_Sucrose = Collar.calculate_Unloading_Sucrose
