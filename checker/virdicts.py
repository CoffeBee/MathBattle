from django_enumfield import enum

class Virdict(enum.Enum):
	WRONG_ANSWER = 0
	ACCEPTED_FOR_EVUALETION = 1
	IN_EVUALETION = 2
	REJECTED = 3
	ACCEPTED = 4
	ACCEPTED_FOR_EVUALETION_IN_CONTEST = 5

