"""
"""

class GoatspeakBlock:
    """
    """
    def __init__(self, fetch_command, query_list, output_command=None):
        """
        """
        self.fetch_command = fetch_command
        self.query_list = query_list
        self.output_command = output_command

    def __repr__(self):
        """
        """
        return f"GoatspeakBlock(fetch_command={self.fetch_command}, query_list={self.query_list}, output_command={self.output_command})"


class Query:
    """
    """
    def __init__(self, graze_commands, fetch_command=None, churn_command=None, deliver_command=None):
        """
        """
        self.fetch_command = fetch_command
        self.graze_commands = graze_commands
        self.churn_command = churn_command
        self.deliver_command = deliver_command

    def __repr__(self):
        """
        """
        return f"Query(graze_commands={self.graze_commands}, fetch_command={self.fetch_command}, churn_command={self.churn_command}, deliver_command={self.deliver_command})"


def main():
    """
    """
    pass


if __name__ == "__main__":
    """
    """
    main()
