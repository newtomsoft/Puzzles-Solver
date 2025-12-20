from enum import Enum, auto


class SubmissionStatus(Enum):
    SUCCESS = auto()
    FAILED_NO_SUCCESS_SELECTOR = auto()
    FAILED_NO_SUBMIT_BUTTON = auto()
    FAILED_SUBMISSION_ERROR = auto()
