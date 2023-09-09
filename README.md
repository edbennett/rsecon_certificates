# RSECon Certificate generator

To generate certificates based on SVG templates.

## Requirements

Pure Python 3.5+,
no library dependencies.

[Inkscape](https://inkscape.org) is required for converting SVG to PDF.

## Usage

To generate certificates for attendees, use

    python certificate.py --attendees_template [template_for_attendee_certificate.svg] --attendees_file [oxford_abstracts_export.csv] --attendees_dir [directory_in_which_to_place_outputs]

To generate certificates for submitters, use

    python certificate.py --talks_template [template_for_submitter_certificate.svg] --talks_file [oxford_abstracts_export.csv] --talks_dir [directory_in_which_to_place_outputs]

To generate certificates for committee members, use

    python certificate.py --committee_template [template_for_committee_certificate.svg] --committee_file [different_filename.csv] --committee_dir [directory_in_which_to_place_outputs]

If `inkscape` is not in your `PATH`,
then you can specify the binary to call by adding

    --inkscape /path/to/your/copy/of/inkscape

To generate only a specific certificate,
rather than all the ones specified in the CSV,
you can add the option

    --only [some_identifier]

`some_identifier` can be any of the identifiers used in the certificate
(e.g. submitter name or submission ID for submissions).
