from cnwheat import model, parameters


class Collar:
    def calculate_Unloading_Sucrose_homogeneity(self, sucrose_roots, sucrose_phloem, mstruct_axis, T_effect_conductivity):
        """Rate of sucrose Unloading from phloem to roots (µmol` C sucrose unloaded g-1 mstruct h-1).


        :param float sucrose_roots: Amount of sucrose in roots (µmol` C)
        :param float sucrose_phloem: Sucrose concentration in phloem (µmol` C g-1 mstruct)
        :param float mstruct_axis: The structural dry mass of the axis (g)
        :param float T_effect_conductivity: Effect of the temperature on the conductivity rate at 20µC (AU)

        :return: Rate of Sucrose Unloading from shoot homogeneous phloem to root homogeneous phloem (µmol` C g-1 mstruct h-1)
        :rtype: float
        """
        # We compute the flow necessary to mean the concentrations between shoot and root phloem, as they are considered as homogeneous.
        print("Computed")
        conc_sucrose_whole_phloem = ((sucrose_roots + sucrose_phloem)
                / (self.mstruct * self.__class__.PARAMETERS.ALPHA + (mstruct_axis - self.mstruct) * parameters.AXIS_PARAMETERS.ALPHA))

        return (conc_sucrose_whole_phloem * self.mstruct * self.__class__.PARAMETERS.ALPHA) - sucrose_roots

    def calculate_Unloading_Sucrose(self, sucrose_roots, sucrose_phloem, mstruct_axis, T_effect_conductivity):
        """Rate of sucrose Unloading from phloem to roots (µmol` C sucrose unloaded g-1 mstruct h-1).

        :param float sucrose_roots: Amount of sucrose in roots (µmol` C)
        :param float sucrose_phloem: Amount of sucrose in phloem (µmol` C)
        :param float mstruct_axis: The structural dry mass of the axis (g)
        :param float T_effect_conductivity: Effect of the temperature on the conductivity rate at 20µC (AU)

        :return: Rate of Sucrose Unloading (µmol` C g-1 mstruct h-1)
        :rtype: float
        """
        print("computed")
        conc_sucrose_phloem_roots = sucrose_roots / (self.mstruct * self.__class__.PARAMETERS.ALPHA)
        conc_sucrose_phloem_shoot = sucrose_phloem / ((mstruct_axis - self.mstruct) * parameters.AXIS_PARAMETERS.ALPHA)
        #: Driving compartment (µmol` C g-1 mstruct)
        driving_sucrose_compartment = max(conc_sucrose_phloem_shoot, conc_sucrose_phloem_roots)
        #: Gradient of sucrose between the roots and the phloem (µmol` C g-1 mstruct)
        diff_sucrose = conc_sucrose_phloem_shoot - conc_sucrose_phloem_roots
        #: Conductance depending on mstruct (g2 µmol`-1 s-1)
        conductance = Roots.PARAMETERS.SIGMA_SUCROSE * Roots.PARAMETERS.BETA * self.mstruct ** (2 / 3) * T_effect_conductivity

        return driving_sucrose_compartment * diff_sucrose * conductance * parameters.SECOND_TO_HOUR_RATE_CONVERSION


model.Roots.calculate_Unloading_Sucrose = Collar.calculate_Unloading_Sucrose
