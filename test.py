import R
from PyQt5.QtWidgets import QMessageBox

j, limit = R.ikine([350, 350,100, 0], [1, 0])
if limit:
    buttonReply = QMessageBox.question(self, 'PyQt5 message', "Do you like PyQt5?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if buttonReply == QMessageBox.Yes:
        print('Yes clicked.')
    else:
        print('No clicked.')

print(j)
print(limit)

