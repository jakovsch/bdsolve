import tkinter.ttk as ttk
from bdsolve.solver.genetic import Player
from bdsolve.ui.common import ArrayView, default_style

class LearnUI:

    def __init__(self):
        self.p = Player()

        self.t = ttk.tkinter.Tk()
        self.t.title('bdsolve - Learning GUI')
        self.t.config(bd=0, relief='flat')
        self.t.geometry('750x500')
        self.t.grid_columnconfigure(0, weight=2)
        self.t.grid_columnconfigure(1, weight=1)
        self.t.grid_rowconfigure(0, weight=1)
        self.s = default_style(self.t)
        self.vars = [
            ttk.tkinter.StringVar(self.t) for _ in range(5)]
        self.ivars = [
            ttk.tkinter.IntVar(self.t) for _ in range(2)]

        self.f1 = ttk.Frame(
            self.t, borderwidth=6, relief='ridge',
            padding='0.3i', style='A.TFrame')
        self.f1.grid(row=0, column=0, sticky='nswe')
        self.f1.grid_columnconfigure(0, weight=1)
        self.f1.grid_rowconfigure(0, weight=5)
        self.f1.grid_rowconfigure(1, weight=1)
        self.f2 = ttk.Frame(
            self.t, borderwidth=6, relief='ridge',
            padding='0.3i', style='B.TFrame')
        self.f2.grid(row=0, column=1, sticky='nswe')
        self.f2.grid_columnconfigure(0, weight=1)

        self.f2_1 = ttk.Labelframe(self.f2, padding='0.1i', text='Controls')
        self.f2_1.grid(row=0, column=0, sticky='nwse')
        self.b1 = ttk.Button(
            self.f2_1, text='Learn',
            command=lambda: [
                self.ivars[0].set(1),
                self.run()
            ])
        self.b1.pack()
        self.b2 = ttk.Button(
            self.f2_1, text='Stop',
            command=lambda: [
                self.ivars[0].set(0)
            ])
        self.b2.pack()
        ttk.Separator(self.f2_1, orient='horizontal').pack()
        self.sb = ttk.Spinbox(
            self.f2_1, from_=10, to=1010, increment=100, width=5)
        self.sb.pack()
        self.sb.set(110)
        self.f2_2 = ttk.Labelframe(self.f2, padding='0.1i', text='Statistics')
        self.f2_2.grid(row=1, column=0, sticky='nwse')
        self.l1 = ttk.Label(self.f2_2, textvariable=self.vars[0])
        self.l1.pack()
        self.l2 = ttk.Label(self.f2_2, textvariable=self.vars[1])
        self.l2.pack()
        self.l3 = ttk.Label(self.f2_2, textvariable=self.vars[2])
        self.l3.pack()
        self.l4 = ttk.Label(self.f2_2, textvariable=self.vars[3])
        self.l4.pack()
        self.l5 = ttk.Label(self.f2_2, textvariable=self.vars[4])
        self.l5.pack()

        self.aw = ArrayView(self.f1, self.p.board.board, 40)
        self.aw.canvas.grid(row=0, column=0, sticky='')
        self.pr = ttk.Progressbar(
            self.f1, orient='horizontal', mode='determinate',
            maximum=self.p.g.pop_count-1, variable=self.ivars[1])
        self.pr.grid(row=1, column=0, sticky='swe')

        self.t.mainloop()

    def run(self):
        self.p.learn()
        self.aw.update()
        self.ivars[1].set(self.p.g.pop_num)
        self.vars[0].set(f'Score: {self.p.score}')
        self.vars[1].set(f'Avg score: {self.p.avg_score}')
        self.vars[2].set(f'Hi score: {self.p.hi_score}')
        self.vars[3].set(f'Current: {self.p.g.pop_num+1}/{self.p.g.pop_count}')
        self.vars[4].set(f'Generation: {self.p.g.gen_num}')
        if self.ivars[0].get():
            self.t.after(int(self.sb.get()), self.run)
