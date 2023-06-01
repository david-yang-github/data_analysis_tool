import getopt
import sys

from .workflow_manager import RemediationManager


# from award_models.workflow_manager import BootManager


def main(argv):
    input_path = ""
    output_path = ""
    project_type = ""
    schema = ""
    test_map = {
        'remediation': RemediationManager
        # 'boot': BootManager,
    }

    try:
        opts, args = getopt.getopt(argv, "hi:o:p:", ["ipath=", "opath=", "project="])
    except getopt.GetoptError:
        print('wage_trust_model.py -i <input_path> | -o <output_path> |  -p <project_type>')
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            print('wage_trust_model.py -i <input_path> | -o <output_path> | -p <project_type>')
            sys.exit()

        elif opt in ('-i', '--ipath'):
            input_path = arg

        elif opt in ('-o', '--opath'):
            output_path = arg

        elif opt in ('-p', '--project'):
            project_type = arg

    if (input_path != "") & (output_path != "") & (project_type != ""):
        print(f'input = "{input_path}"..output= "{output_path}"..project_type = "{project_type}"..schema = "{schema}"')
        test_obj = test_map[project_type.lower()](input_path, output_path)
        test_obj.run_simulation()

    else:
        print('You have to provide input file path!')
        print('wage_trust_model.py -i <input_path> | -o <output_path> | -p <project_type>')
        sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
