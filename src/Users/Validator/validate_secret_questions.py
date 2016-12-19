from src.models.Records.record import Records
from src.utilities.common import (check_passwd_hash,
	                              create_passwd_hash,
	                              get_questions)

class ValidiateSecretQuestions(object):
	"""ValidiateSecretQuestions(class)
	The class validates whether the secret answers from the user's
	are correct.
	"""
	def __init__(self, form):
		self.form = form

	def _get_answers(self):
		"""Returns the users secret questions"""
		if not self.form.username.data:
			return None
		query = {'username' : str(self.form.username.data.lower())}
		return Records.get_secret_answers(collection='forgotten_password', query=query)

	def validate_answers(self):
	    """Validiates the users secret answers"""
	    rec_obj = self._get_answers()
	    form = self.form
	    if rec_obj != None:
	    	question_one, question_two = get_questions()
	    	ans_one = check_passwd_hash(form.maiden_name.data.lower(), rec_obj.get(question_one))
	    	ans_two = check_passwd_hash(form.leisure.data.lower(), rec_obj.get(question_two))
	    	return True if ans_one and ans_two else False
	    return False
