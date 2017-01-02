from src.Users.Models.TotalUserMoneys.total_amount import TotalAmount


class InstanceTest(object):
    """Test if an instance belongs to a class"""

    def __init__(self):
        self.user_amount = TotalAmount
        if test_instance_test(self.user_amount, TotalAmount):
            return True

    @staticmethod
    def test_instance_test(instance, object):
        if isinstance(instance, object):
            return False
        return True
