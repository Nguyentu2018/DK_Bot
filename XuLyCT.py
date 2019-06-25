def ProgramTherad():
    a = w.edit_Program.toPlainText()
    a = a.upper()
    ct = a.split()
    print(ct)
    SL_Dat = w.Step_SL.value()
    SL = int(w.edit_SL.text())
    try:
        for i in range(SL, SL_Dat):
            for n in range(0, len(ct)):
                line = ct[n]
                if line == 'K1':
                    print('Nâng khuôn ')
                    w.lb_Stt.setText('Nâng khuôn')
                    ecd.send('A1B0*')

                if line == 'K0':
                    print('Hạ khuôn ')
                    w.lb_Stt.setText('Hạ khuôn')
                    ecd.send('A1B1*')

                if line[0] == 'A':
                    goc = line.lstrip('A')
                    print('Bẻ trước ' + goc)
                    w.lb_Stt.setText('Bẻ trước ' + goc)
                    g2.send('g90g01x' + goc + 'f10000')
                    while w.lb_stt.text() != 'Next':
                        pass

                if line[0] == 'B':
                    goc = line.lstrip('B')
                    print('Bẻ sau ' + goc)
                    w.lb_Stt.setText('Bẻ sau ' + goc)
                    g2.send('g90g01x' + goc + 'f10000')
                    while w.lb_stt.text() != 'Next':
                        pass

                if line[0] == 'X':
                    goc = line.lstrip('X')
                    print('Xoay ' + goc)
                    w.lb_Stt.setText('Xoay ' + goc)
                    g2.send('g90g01Y' + goc + 'f1000')
                    while w.lb_stt.text() != 'Next':
                        pass

                if line[0] == 'D':
                    feed = line.lstrip('D')
                    print('Đẩy dây ' + feed)
                    w.lb_Stt.setText('Đẩy dây ' + feed)
                    g2.send('g90g01Z' + feed + 'f1000')
                    while w.lb_stt.text() != 'Next':
                        pass

                time.sleep(0.3)
    except:
        print("END")
    print('Stop....')
    w.lb_Stt.setText('Stop ')