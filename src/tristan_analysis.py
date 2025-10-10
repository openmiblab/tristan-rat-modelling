from methods import plot, analysis


if __name__ == '__main__':

    analysis.six_compound_effect_sizes()
    plot.six_compound_data()
    plot.six_compound_effect_sizes()

    analysis.reproducibility()
    plot.reproducibility()

    analysis.chronic_cyclosporine()
    plot.chronic_cyclosporine()

    analysis.chronic_rifampicin()
    plot.chronic_rifampicin()

    plot.bosentan_data()
    plot.rifampicin_data()
    plot.field_strength_data()