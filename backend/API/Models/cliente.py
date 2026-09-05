class Cliente:

    def __init__(self, CLI_ID, CLI_UUID, CLI_PER_ID):
        self.CLI_ID = CLI_ID
        self.CLI_UUID = CLI_UUID
        self.CLI_PER_ID = CLI_PER_ID

    def to_dic(self):
        return {
            "id": self.CLI_ID,
            "uuid": self.CLI_UUID,
            "per_id": self.CLI_PER_ID
        }
    