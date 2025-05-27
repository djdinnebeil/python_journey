from pydantic import BaseModel

class TestingClass(BaseModel):
    testing_class: str
    testing_class2: str

new_test = TestingClass(testing_class=4,testing_class2='4')
new_test.testing_class = '4'
print(new_test.testing_class)