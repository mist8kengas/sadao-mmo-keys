from datetime import datetime
import keyboard
import tkinter as tk


class config:
    def get_keys():
        f = open('keys.txt', 'r')
        keys = f.readlines(1)[0].split(',')
        keys_fmt = {}

        for key in keys:
            key_fmt = key.upper()
            keys_fmt[key_fmt] = key_fmt
        return keys_fmt


count = 0
keyhist = []
do_log = True


class Window:
    def tk_root(self):
        return self.root

    # components
    def component_keyhist(self):
        return self.tk_keyhist

    def count_value(self):
        return self.tk_count_value_str

    def __init__(self):
        # window
        self.root = tk.Tk()
        self.root.title('Sadao MMO Keys')
        self.root.minsize(width=300, height=200)
        self.root.attributes('-topmost', True)

        self._setupc_count_label()
        self._setupc_count_value()
        self._setupc_toggle()
        self._setupc_keylog()

    # setup components
    def _setupc_count_label(self):
        # count label
        tk_count_label = tk.Label(
            self.root, text=f'Skill Count', font=('Consolas', 18))
        tk_count_label.pack(padx=10, pady=(10, 0))

    def _setupc_count_value(self):
        # count value
        self.tk_count_value_str = tk.StringVar(self.root, count)
        tk_count_value = tk.Label(
            self.root, textvariable=self.tk_count_value_str, font=('Consolas', 32))
        tk_count_value.pack(padx=10, pady=(0, 10))

    def _setupc_toggle(self):
        # toggle button
        tk_toggle_label = tk.StringVar(self.root, 'Disable')

        def toggle_handler():
            global do_log
            if do_log:
                do_log = False
                self.root.attributes('-topmost', False)
                tk_toggle_label.set('Enable')
            else:
                do_log = True
                self.root.attributes('-topmost', True)
                tk_toggle_label.set('Disable')

        tk_toggle = tk.Button(
            self.root, textvariable=tk_toggle_label, command=toggle_handler)
        tk_toggle.pack()

    def _setupc_keylog(self):
        # key log
        self.tk_keyhist = tk.Text(self.root)
        self.tk_keyhist.pack(padx=10, pady=10)
        self.tk_keyhist.insert('1.0', 'Waiting for input...')
        self.tk_keyhist['state'] = 'disabled'


def main():
    # window
    window = Window()

    # logger
    keys = config.get_keys()

    def logger(log: keyboard.KeyboardEvent):
        key = str.upper(log.name)
        id = log.scan_code

        global count
        if keys.get(key) and do_log:
            if count < 2:
                count += 1
            elif count == 2:
                count = 0

            # add key to history
            keyhist.append({'time': log.time, 'key': key})

            # update window
            window.count_value().set(count)

            window.component_keyhist()['state'] = 'normal'
            window.component_keyhist().delete('1.0', tk.END)
            for i in range(len(keyhist)):
                history = keyhist[i]
                time = datetime.fromtimestamp(history['time']).time()
                key = history['key']
                window.component_keyhist().insert(
                    f'{i + 1}.0', f'{time}: {key}\n')
            window.component_keyhist().yview_moveto(1)
            window.component_keyhist()['state'] = 'disabled'

    keyboard.on_press(logger)
    # keyboard.wait()
    window.tk_root().mainloop()


if __name__ == '__main__':
    main()
