# EOCSI Hackathon 2022 <img align="right" src="resources/csiro_easi_logo.png">

Notebooks and materials for the EOCSI Hackathon 2022, https://frontiersi.com.au/climate-innovation-hack/

- Use the examples in these notebooks to build your own data analysis and applications.
- These notebooks have been adapted and written for [CSIRO's EASI SE Asia
platform](https://research.csiro.au/cceo/building-new-earth-observation-capabilities-in-the-south-east-asian-region/).

<figure align="right">
    <img src="resources/lake-tempe-landsat-rgb.png">
    <figcaption><i>Lake Tempe, Indonesia. Landsat-8 (2020-03-13) RGB</i></figcaption>
</figure>

## Overview

#### *.ipynb

- Notebooks that introduce aspects of EASI, Dask and the Open Data Cube libraries.
- Work through these as a Training exercise, and refer back to them for examples.

#### datasets/
- Demonstrations for accessing and using EASI data products.
- Adapt or copy from these for your own work.

#### case-studies/
- Science applications and examples.

#### html/
- HTML version of each notebook for easy browsing.

#### tools/
- Helper scripts used in the these notebooks.

#### resources/

- Supplementary files and images used in the EASI notebooks.

#### bin/

- Scripts for managing and contributing to the repository.

## Contributing

Contributions are welcome.

A `pre-commit` hook is provided in `/bin`. For each notebook committed:

1. Create an HTML copy of the notebook into `html/`.
1. Strip *outputs* from the notebook to limit the size of the repository.

The `apply_hooks.sh` script creates a symlink to `bin/pre-commit`.

```bash
# Run this in your local repository
sh bin/apply_hooks.sh
```

For contributors:

1. Apply the pre-commit hook.
1. Run each notebook (that has been updated) to populate the figures, tables and other *outputs* as you want them.
1. For each new notebook add a link to `html/readme.md`.
1. `git add` and `git commit`.
1. If eveything looks ok, `git push` to your fork of this repository and create a *pull request*.

#### pre-commit-config.yaml
Work in progress (not configured yet).


## License

Apache License 2.0, <https://www.apache.org/licenses/LICENSE-2.0>.
