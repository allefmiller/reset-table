from tkinter import messagebox
import database as db
from tkinter import *

root = Tk()
root.title('Reset Table RUBI')
root.geometry("260x230")

verify_table_log = db.verify_table_exists('reset_table_RUBI_log')

def create_table_log():
    return_value = db.execute_sql("""
        CREATE TABLE [dbo].[reset_table_rubi_log](
            [id] INT IDENTITY(1,1),  
            [tabela] VARCHAR (50),
            [data] DATETIME
            PRIMARY KEY ([id])
        )
    """)
    if return_value['status'] != 0:
        messagebox.showerror('Erro!', 'Erro ao criar a tabela de log'+ '\n          Erro: ' + return_value['message'])
    else:
        messagebox.showinfo('Sucesso!', 'Tabela de log criada com sucesso!')
        button_create_table_log.destroy()

def clear_table(table):
    verify_table_log = db.verify_table_exists('reset_table_RUBI_log')
    if verify_table_log['status'] == 1:
        return_value = db.execute_sql(f"insert into [dbo].[reset_table_rubi_log] values('{table}',GETDATE())")
        if return_value['status'] != 0:
            messagebox.showerror('Erro!', 'Erro ao criar a tabela de log'+ '\n          Erro: ' + return_value['message'])
    
    return_value = db.execute_sql(f"DELETE FROM {table}")
    if return_value['status'] == 0:
        messagebox.showinfo('Sucesso!', 'A tabela ' + table + ' foi limpa! \n          Registros afetados: ' + str(return_value['message']))
    else:
        messagebox.showerror('Erro!', 'Erro ao limpar a tabela ' + table + '\n          Erro: ' + return_value['message'])
    
label_table_one = Label(root, text= 'Tabela : ' + db.TABLE_ONE)
label_table_one.pack(pady=10)
button_clear_table_one= Button(root, text="Limpar Tabela", command=lambda: clear_table(db.TABLE_ONE))
button_clear_table_one.pack(pady=10)

label_table_two = Label(root, text='Tabela : ' + db.TABLE_TWO)
label_table_two.pack(pady=10)
button_clear_table_two= Button(root, text="Limpar Tabela", command= lambda: clear_table(db.TABLE_TWO))
button_clear_table_two.pack(pady=10)

if verify_table_log['status'] == 0:
    button_create_table_log= Button(root, text="Criar tabela de log", command= lambda: create_table_log())
    button_create_table_log.pack(pady=10)


root.mainloop()
