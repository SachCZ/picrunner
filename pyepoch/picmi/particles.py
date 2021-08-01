from copy import copy

import picmistandard


class Species(picmistandard.PICMI_Species):
    def init(self, kw):
        pass


class MultiSpecies(picmistandard.PICMI_MultiSpecies):
    def init(self, kw):
        pass


picmistandard.PICMI_MultiSpecies.Species_class = Species


class AnalyticDistribution(picmistandard.PICMI_AnalyticDistribution):
    def init(self, kw):
        pass

    def get_parsed_density_expresion(self):
        expression = copy(self.density_expression)

        for key in self.user_defined_kw:
            expression = expression.replace(key, "{}".format(self.user_defined_kw[key]))

        expression = expression.replace("where", "if")
        expression = expression.replace("&", "and")
        expression = expression.replace(">", "gt")
        expression = expression.replace("<", "lt")
        expression = expression.replace("==", "eq")
        expression = expression.replace("|", "or")
        return expression


class GriddedLayout(picmistandard.PICMI_GriddedLayout):
    def init(self, kw):
        pass
