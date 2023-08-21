class RecordNotFoundError(Exception):
    def __init__(self, record_id):
        self.record_id = record_id
        self.message = f'Record with id {record_id} was not found'
        super().__init__(self.message)
