from csv import DictReader
from html import escape
import subprocess


SETTINGS = {"inkscape": "inkscape"}


def get_things(filename, mapper):
    with open(filename, "r", newline="") as f:
        reader = DictReader(f)
        for thing in reader:
            yield mapper(thing)


def get_talks(talks_file):
    return get_things(
        talks_file,
        lambda talk: {
            "id": talk["Submission Id"],
            "name": f'{talk["Submitter first name"]} {talk["Submitter last name"]}',
            "eventtype": talk["Event type"].split()[0].lower(),
            "title": talk["Title"],
        },
    )


def get_attendees(attendees_file):
    return get_things(
        attendees_file,
        lambda attendee: {
            "id": attendee["Ticket number"],
            "name": attendee["Full Name"],
        },
    )


def get_committee_members(committee_file):
    return get_things(
        committee_file,
        lambda member: {
            "name": member["Name"],
            "role": member["Role"],
        },
    )


def escape_attrs(attrs):
    return {k: escape(v) for k, v in attrs.items()}


def process_things(
    thing_getter, things_file, template_file, basename_formatter, only=None
):
    template = template_file.read()
    template_file.close()

    for thing in thing_getter(things_file):
        if only is not None and only not in thing.values():
            continue

        file_basename = basename_formatter.format(**thing)
        print(file_basename)
        with open(f"{file_basename}.svg", "w") as f:
            print(template.format(**escape_attrs(thing)), file=f)
        subprocess.run(
            [
                SETTINGS["inkscape"],
                f"--export-filename={file_basename}.pdf",
                "--export-overwrite",
                f"{file_basename}.svg",
            ]
        )


def main():
    from argparse import ArgumentParser, FileType

    parser = ArgumentParser()
    parser.add_argument("--talks_template", type=FileType("r"), default=None)
    parser.add_argument("--attendees_template", type=FileType("r"), default=None)
    parser.add_argument("--committee_template", type=FileType("r"), default=None)
    parser.add_argument("--talks_file", default=None)
    parser.add_argument("--attendees_file", default=None)
    parser.add_argument("--committee_file", default=None)
    parser.add_argument("--talks_dir", default=".")
    parser.add_argument("--attendees_dir", default=".")
    parser.add_argument("--committee_dir", default=".")
    parser.add_argument("--inkscape", default=None)
    parser.add_argument("--only", default=None)
    args = parser.parse_args()

    if args.talks_template or args.talks_file:
        assert args.talks_template and args.talks_file
    if args.attendees_template or args.attendees_file:
        assert args.attendees_template and args.attendees_file

    if args.inkscape is not None:
        SETTINGS["inkscape"] = args.inkscape

    if not (args.talks_template or args.attendees_template or args.committee_template):
        print("Nothing to do.")

    if args.attendees_template:
        process_things(
            get_attendees,
            args.attendees_file,
            args.attendees_template,
            f"{args.attendees_dir}/{{id}} {{name}}",
            only=args.only,
        )

    if args.talks_template:
        process_things(
            get_talks,
            args.talks_file,
            args.talks_template,
            f"{args.talks_dir}/{{id}} {{name}}",
            only=args.only,
        )

    if args.committee_template:
        process_things(
            get_committee_members,
            args.committee_file,
            args.committee_template,
            f"{args.committee_dir}/{{name}}",
            only=args.only,
        )


if __name__ == "__main__":
    main()
