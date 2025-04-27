# pylint: disable=missing-module-docstring, missing-function-docstring, invalid-name,line-too-long

"""This script will ask user to provide as an input the NRB ticket # in oreder to be returned and used for further processing"""


def user_input() -> str:
    """_summary_: This function will ask user to provide the NRB ticket # in oreder to be returned and used for further processing

    Returns:
        str: NRB ticket # provided by the user
    """

    # Ask user to provide the NRB ticket #
    nrb_ticket = input("Please provide the NRB ticket # (e.g. NRBxxxxxxxxx): ")
    print(f"NRB ticket # provided: {nrb_ticket}")
    return nrb_ticket


if __name__ == "__main__":
    user_input()
