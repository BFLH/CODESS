import tkinter as tk
from tkinter import ttk, messagebox
import database as db
import receipt
import re

# --- Paleta de Colores "Citrus POS" ---
COLOR_BG = "#F5F5F5"           # Fondo claro, casi blanco
COLOR_FRAME = "#FFFFFF"        # Blanco puro para páneles
COLOR_TEXT = "#212121"         # Texto oscuro para alta legibilidad
COLOR_PRIMARY = "#8E44AD"      # Púrpura elegante
COLOR_SUCCESS = "#27AE60"      # Verde esmeralda
COLOR_DANGER = "#C0392B"       # Rojo ladrillo
COLOR_HEADER_BG = "#9B59B6"    # Púrpura más claro para cabeceras
FONT_FAMILY = "Segoe UI"

def treeview_sort_column(tree, col, reverse):
    data = [(tree.set(k, col), k) for k in tree.get_children('')]
    try:
        data.sort(key=lambda t: float(t[0].replace('$', '').replace(',', '')), reverse=reverse)
    except ValueError:
        data.sort(reverse=reverse)
    for index, (val, k) in enumerate(data):
        tree.move(k, '', index)
    tree.heading(col, command=lambda: treeview_sort_column(tree, col, not reverse))

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        db.setup_database()
        self.show_login_window()

    def show_login_window(self):
        self.login_window = LoginPage(self, self.on_login_success)
    
    def on_login_success(self, user_data):
        self.login_window.destroy()
        self.main_app = MainPage(self, user_data)

class LoginPage(tk.Toplevel):
    def __init__(self, master, login_callback):
        super().__init__(master)
        self.title("Citrus POS - Iniciar Sesión")
        self.geometry("400x500")
        self.configure(bg=COLOR_BG)
        self.login_callback = login_callback

        main_frame = tk.Frame(self, bg=COLOR_BG, padx=40, pady=40)
        main_frame.pack(expand=True, fill="both")

        ttk.Label(main_frame, text="Citrus POS", font=(FONT_FAMILY, 28, "bold"), foreground=COLOR_PRIMARY, background=COLOR_BG).pack(pady=(0, 10))
        ttk.Label(main_frame, text="Bienvenido de nuevo", font=(FONT_FAMILY, 14), foreground=COLOR_TEXT, background=COLOR_BG).pack(pady=(0, 40))

        ttk.Label(main_frame, text="Usuario", font=(FONT_FAMILY, 12), background=COLOR_BG).pack(anchor="w")
        self.username_entry = ttk.Entry(main_frame, font=(FONT_FAMILY, 12), width=30)
        self.username_entry.pack(pady=5, ipady=5)

        ttk.Label(main_frame, text="Contraseña", font=(FONT_FAMILY, 12), background=COLOR_BG).pack(anchor="w", pady=(10, 0))
        self.password_entry = ttk.Entry(main_frame, show="*", font=(FONT_FAMILY, 12), width=30)
        self.password_entry.pack(pady=5, ipady=5)
        self.password_entry.bind('<Return>', lambda e: self.login())

        login_button = tk.Button(main_frame, text="Ingresar", command=self.login, bg=COLOR_PRIMARY, fg=COLOR_FRAME, font=(FONT_FAMILY, 12, "bold"), relief="flat", width=25, height=2)
        login_button.pack(pady=30)
        
        self.protocol("WM_DELETE_WINDOW", self.master.destroy)

    def login(self):
        user_data = db.verify_user(self.username_entry.get(), self.password_entry.get())
        if user_data:
            self.login_callback({"id": user_data[0], "username": self.username_entry.get(), "role": user_data[1]})
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")  

class MainPage(tk.Toplevel):
    def __init__(self, master, user_data):
        super().__init__(master)
        self.master = master
        self.user_data = user_data
        self.title(f"Citrus POS - Panel Principal ({self.user_data['username']})")
        self.geometry("800x600")
        self.configure(bg=COLOR_BG)
        self.create_menu()

        welcome_frame = tk.Frame(self, bg=COLOR_BG)
        welcome_frame.pack(expand=True, fill="both")
        ttk.Label(welcome_frame, text="Citrus POS", font=(FONT_FAMILY, 48, "bold"), foreground=COLOR_PRIMARY, background=COLOR_BG).pack(pady=(100, 10))
        ttk.Label(welcome_frame, text="Seleccione una opción del menú para comenzar", font=(FONT_FAMILY, 16), background=COLOR_BG).pack()
        
        self.protocol("WM_DELETE_WINDOW", self.master.destroy)

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Cerrar Sesión", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.master.destroy)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        sales_menu = tk.Menu(menubar, tearoff=0)
        sales_menu.add_command(label="Nuevo Punto de Venta", command=self.open_pos_window)
        sales_menu.add_command(label="Historial de Ventas", command=self.open_history_window)
        menubar.add_cascade(label="Ventas", menu=sales_menu)
        if self.user_data['role'] == 'Gerente':
            management_menu = tk.Menu(menubar, tearoff=0)
            management_menu.add_command(label="Gestionar Productos", command=self.open_products_window)
            management_menu.add_command(label="Gestionar Usuarios", command=self.open_users_window)
            menubar.add_cascade(label="Gestión", menu=management_menu)

    def open_pos_window(self): POSWindow(self, self.user_data)
    def open_products_window(self): ProductsWindow(self)
    def open_users_window(self): UsersWindow(self)
    def open_history_window(self): HistoryWindow(self)
    def logout(self):
        self.destroy()
        self.master.show_login_window() # type: ignore

# Clase Base para las ventanas con tablas
class BaseTableWindow(tk.Toplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        self.configure(bg=COLOR_BG)
        self.setup_styles()

    def setup_styles(self):
        style = ttk.Style(self)
        style.configure("Treeview.Heading", 
                        font=(FONT_FAMILY, 11, "bold"), 
                        background=COLOR_HEADER_BG, 
                        foreground=COLOR_TEXT,  
                        relief="flat")
        style.map("Treeview.Heading", background=[('active', COLOR_PRIMARY)])
        style.configure("Treeview", 
                        rowheight=25, 
                        fieldbackground=COLOR_FRAME, 
                        background=COLOR_FRAME, 
                        foreground=COLOR_TEXT)
        
class POSWindow(BaseTableWindow):
    def __init__(self, master, user_data):
        super().__init__(master, "Punto de Venta")
        self.geometry("900x600")
        self.user_data = user_data
        self.cart = []
        
        client_frame = tk.Frame(self, bg=COLOR_BG, padx=15, pady=5)
        client_frame.pack(fill="x")
        ttk.Label(client_frame, text="Cliente:", font=(FONT_FAMILY, 11, "bold"), background=COLOR_BG).grid(row=0, column=0, padx=(0, 10))
        self.client_name = ttk.Entry(client_frame, width=25, font=(FONT_FAMILY, 11))
        self.client_name.grid(row=0, column=1, padx=5)
        ttk.Label(client_frame, text="Cédula:", font=(FONT_FAMILY, 11, "bold"), background=COLOR_BG).grid(row=0, column=2, padx=(20, 10))
        self.client_id = ttk.Entry(client_frame, width=15, font=(FONT_FAMILY, 11))
        self.client_id.grid(row=0, column=3, padx=5)
        ttk.Label(client_frame, text="Teléfono:", font=(FONT_FAMILY, 11, "bold"), background=COLOR_BG).grid(row=0, column=4, padx=(20, 10))
        self.client_phone = ttk.Entry(client_frame, width=15, font=(FONT_FAMILY, 11))
        self.client_phone.grid(row=0, column=5, padx=5)
    
        add_frame = tk.Frame(self, bg=COLOR_BG, padx=15, pady=15)
        add_frame.pack(fill="x")
        add_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(add_frame, text="Producto:", font=(FONT_FAMILY, 11, "bold"), background=COLOR_BG).grid(row=0, column=0, padx=(0, 10))
        self.product_combo = ttk.Combobox(add_frame, state="readonly", font=(FONT_FAMILY, 11))
        self.product_combo.grid(row=0, column=1, padx=10, sticky="ew")
        self.populate_products()

        ttk.Label(add_frame, text="Cantidad:", font=(FONT_FAMILY, 11, "bold"), background=COLOR_BG).grid(row=0, column=2, padx=(20, 10))
        self.quantity_entry = ttk.Entry(self, width=8, font=(FONT_FAMILY, 11), justify='center')
        self.quantity_entry.grid(in_=add_frame, row=0, column=3, padx=10)
        self.quantity_entry.insert(0, "1")
        
        tk.Button(add_frame, text="Añadir", command=self.add_to_cart, bg=COLOR_PRIMARY, fg=COLOR_FRAME, relief="flat", font=(FONT_FAMILY, 10, "bold")).grid(row=0, column=4, padx=(20, 0), ipady=3)

        tree_frame = tk.Frame(self, bg=COLOR_FRAME, padx=15, pady=15)
        tree_frame.pack(fill="both", expand=True, pady=10, padx=15)
        
        self.tree = ttk.Treeview(tree_frame, columns=("SKU", "Producto", "Cant.", "Precio", "Subtotal"), show="headings")
        self.tree.pack(fill="both", expand=True)

        bottom_frame = tk.Frame(self, bg=COLOR_BG, padx=15, pady=15)
        bottom_frame.pack(fill="x")
        self.total_label = ttk.Label(bottom_frame, text="Total: $0.00", font=(FONT_FAMILY, 18, "bold"), background=COLOR_BG)
        self.total_label.pack(side="left")
        
        tk.Button(bottom_frame, text="Finalizar Venta", command=self.finalize_sale, bg=COLOR_SUCCESS, fg=COLOR_FRAME, relief="flat", font=(FONT_FAMILY, 12, "bold")).pack(side="right", padx=(10, 0))
        tk.Button(bottom_frame, text="Vaciar Carrito", command=self.clear_cart, bg=COLOR_DANGER, fg=COLOR_FRAME, relief="flat", font=(FONT_FAMILY, 11, "bold")).pack(side="right")
        self.setup_tree_columns()
        
    def setup_tree_columns(self):
        self.tree.heading("SKU", text="SKU")
        self.tree.column("SKU", width=120)
        self.tree.heading("Producto", text="Producto")
        self.tree.column("Producto", width=350)
        self.tree.heading("Cant.", text="Cant.")
        self.tree.column("Cant.", width=60, anchor="center")
        self.tree.heading("Precio", text="Precio Unit.")
        self.tree.column("Precio", width=100, anchor="e")
        self.tree.heading("Subtotal", text="Subtotal")
        self.tree.column("Subtotal", width=100, anchor="e")
    
    def populate_products(self):
        self.products_data = db.get_all_products()
        product_names = [f"{p[1]} (Stock: {p[3]})" for p in self.products_data if p[3] > 0]
        self.product_combo['values'] = product_names
        if product_names:
            self.product_combo.current(0)

    def add_to_cart(self):
        selected_product_str = self.product_combo.get()
        if not selected_product_str:
            return
        try:
            quantity = int(self.quantity_entry.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número.", parent=self)
            return
        if quantity <= 0:
            messagebox.showerror("Error", "La cantidad debe ser un número positivo mayor a cero.", parent=self)
            return
        product_data = next((p for p in self.products_data if f"{p[1]} (Stock: {p[3]})" == selected_product_str), None)
        if not product_data:
            return
        sku, name, price, stock = product_data

        # Verificar si el producto ya está en el carrito
        cart_item = next((item for item in self.cart if item['sku'] == sku), None)
        total_quantity = quantity
        if cart_item:
            total_quantity += cart_item['quantity']
        if total_quantity > stock:
            messagebox.showerror("Error de Stock", f"Stock insuficiente para '{name}'. Disponible: {stock - (cart_item['quantity'] if cart_item else 0)}", parent=self)
            return
        if cart_item:
            cart_item['quantity'] += quantity
        else:
            self.cart.append({"sku": sku, "name": name, "quantity": quantity, "price": price})
        self.update_cart_display()

    def update_cart_display(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        total = sum(item['price'] * item['quantity'] for item in self.cart)
        for item in self.cart:
            subtotal = item['quantity'] * item['price']
            self.tree.insert("", "end", values=(item['sku'], item['name'], item['quantity'], f"${item['price']:.2f}", f"${subtotal:.2f}"))
        self.total_label.config(text=f"Total: ${total:.2f}")

    def clear_cart(self):
        if self.cart and messagebox.askyesno("Confirmar", "¿Desea vaciar el carrito?", parent=self):
            self.cart.clear()
            self.update_cart_display()
    
    def finalize_sale(self):
        if not self.cart:
            messagebox.showwarning("Advertencia", "El carrito está vacío.", parent=self)
            return
        name = self.client_name.get().strip()
        cid = self.client_id.get().strip()
        phone = self.client_phone.get().strip()
        # Validaciones
        if not name or not cid or not phone:
            messagebox.showerror("Error", "Debe ingresar nombre, cédula y teléfono del cliente.", parent=self)
            return
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', name):
            messagebox.showerror("Error", "El nombre del cliente solo debe contener letras y espacios.", parent=self)
            return
        # Cedula y telefono: solo números, puntos y guiones, al menos un número
        if not re.match(r'^[0-9.\-]+$', cid) or not re.search(r'\d', cid):
            messagebox.showerror("Error", "La cédula solo puede contener números, puntos y guiones, y debe tener al menos un número.", parent=self)
            return
        if not re.match(r'^[0-9.\-]+$', phone) or not re.search(r'\d', phone):
            messagebox.showerror("Error", "El teléfono solo puede contener números, puntos y guiones, y debe tener al menos un número.", parent=self)
            return
        if not messagebox.askyesno("Confirmar Venta", f"El total es {self.total_label.cget('text')}. ¿Desea continuar?", parent=self):
            return
        sale_id, total_amount = db.record_sale(self.user_data['id'], self.cart, name, cid, phone)
        if sale_id:
            messagebox.showinfo("Venta Exitosa", f"Venta #{sale_id} registrada con éxito a {name}.", parent=self)
            receipt.generate_receipt(
                sale_id, self.cart, total_amount, self.user_data['username'],
                client_name=name, client_id=cid, client_phone=phone
            )
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo registrar la venta.", parent=self)

class GenericCRUDWindow(BaseTableWindow):
    def __init__(self, master, title, columns, fields):
        super().__init__(master, title)
        self.geometry("950x500")
        
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        tree_container = tk.Frame(self, bg=COLOR_FRAME, padx=15, pady=15)
        tree_container.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.tree = ttk.Treeview(tree_container, columns=list(columns.keys()), show="headings")
        for col_id, col_text in columns.items():
            self.tree.heading(col_id, text=col_text)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)

        form_container = tk.Frame(self, bg=COLOR_FRAME, padx=15, pady=15)
        form_container.grid(row=0, column=1, sticky="nsew", pady=15, padx=(0, 15))
        ttk.Label(form_container, text="Detalles", font=(FONT_FAMILY, 14, "bold"), background=COLOR_FRAME, foreground=COLOR_PRIMARY).pack(anchor="w", pady=(0, 10))
        self.entries = {}
        for field_name, field_type in fields.items():
            ttk.Label(form_container, text=f"{field_name}:", background=COLOR_FRAME).pack(anchor="w", pady=(10, 2))
            if field_type == "combo":
                entry = ttk.Combobox(form_container, values=['Trabajador', 'Gerente'], state="readonly", font=(FONT_FAMILY, 11))
                entry.set('Trabajador')
            else:
                entry = ttk.Entry(form_container, font=(FONT_FAMILY, 11), width=35)
            entry.pack(anchor="w", fill="x", ipady=3)
            self.entries[field_name] = entry

        btn_frame = tk.Frame(form_container, bg=COLOR_FRAME)
        btn_frame.pack(pady=20, fill="x", side="bottom")
        tk.Button(btn_frame, text="Añadir", bg=COLOR_SUCCESS, fg="white", relief="flat", command=self.add_item).pack(side="left", expand=True, padx=2, ipady=4)
        tk.Button(btn_frame, text="Actualizar", bg=COLOR_PRIMARY, fg="white", relief="flat", command=self.update_item).pack(side="left", expand=True, padx=2, ipady=4)
        tk.Button(btn_frame, text="Eliminar", bg=COLOR_DANGER, fg="white", relief="flat", command=self.delete_item).pack(side="left", expand=True, padx=2, ipady=4)
        tk.Button(btn_frame, text="Limpiar", bg="#bdc3c7", fg="#2c3e50", relief="flat", command=self.clear_form).pack(side="left", expand=True, padx=2, ipady=4)

    def on_item_select(self, event):
        selected_items = self.tree.selection()
        if not selected_items:
            return
        values = self.tree.item(selected_items[0], "values")
        self.populate_form(values)

    def populate_form(self, values):
        raise NotImplementedError
    def add_item(self):
        raise NotImplementedError
    def update_item(self):
        raise NotImplementedError
    def delete_item(self):
        raise NotImplementedError
    def clear_form(self):
        for entry in self.entries.values():
            if isinstance(entry, ttk.Combobox):
                entry.set('Trabajador')
            else:
                entry.delete(0, 'end')

class ProductsWindow(GenericCRUDWindow):
    def __init__(self, master):
        super().__init__(
            master,
            "Gestión de Productos",
            {"sku": "SKU", "name": "Nombre", "price": "Precio", "stock": "Stock"},
            {"Nombre": "text", "Precio": "text", "Stock": "text"}
        )
        self.tree.config(selectmode="browse")
        # Encabezados con sort
        for col, text in zip(("sku", "name", "price", "stock"), ("SKU", "Nombre", "Precio", "Stock")):
            self.tree.heading(col, text=text, command=lambda _col=col: treeview_sort_column(self.tree, _col, False))
        self.refresh_treeview()
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_item_select)
        self.tree.bind("<Double-1>", self.on_tree_item_double_click)

    def refresh_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for p in db.get_all_products():
            self.tree.insert("", "end", values=(p[0], p[1], f"${p[2]:.2f}", p[3]))
        children = self.tree.get_children()
        if children:
            self.tree.selection_set(children[0])
            self.tree.focus(children[0])
            self.populate_form(self.tree.item(children[0], "values"))

    def populate_form(self, values):
        self.clear_form()
        self.entries['Nombre'].insert(0, values[1])
        self.entries['Precio'].insert(0, values[2].replace('$', ''))
        self.entries['Stock'].insert(0, values[3])

    def on_tree_item_select(self, event):
        selected = self.tree.selection()
        print("DEBUG on_tree_item_select:", selected)
        if selected:
            values = self.tree.item(selected[0], "values")
            self.populate_form(values)

    def on_tree_item_double_click(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            print("DEBUG on_tree_item_double_click, seleccionando:", item)
            values = self.tree.item(item, "values")
            self.populate_form(values)

    def add_item(self):
        try:
            name = self.entries['Nombre'].get()
            price = float(self.entries['Precio'].get())
            stock = int(self.entries['Stock'].get())
        except ValueError:
            messagebox.showerror("Error", "Precio y Stock deben ser números.", parent=self)
            return
        if not name:
            messagebox.showerror("Error", "El nombre es obligatorio.", parent=self)
            return
        # El nombre puede contener cualquier carácter, no se valida con regex
        if price <= 0:
            messagebox.showerror("Error", "El precio debe ser un número positivo mayor a cero.", parent=self)
            return
        if stock <= 0:
            messagebox.showerror("Error", "El stock debe ser un número positivo mayor a cero.", parent=self)
            return
        db.add_product(name, price, stock)
        self.refresh_treeview()
        self.clear_form()

    def update_item(self):
        selected = self.tree.selection()
        print("DEBUG selección update:", selected)
        if not selected:
            messagebox.showerror("Error", "Seleccione un producto.", parent=self)
            return
        sku = self.tree.item(selected[0], "values")[0]
        try:
            name = self.entries['Nombre'].get()
            price = float(self.entries['Precio'].get())
            stock = int(self.entries['Stock'].get())
        except ValueError:
            messagebox.showerror("Error", "Precio y Stock deben ser números.", parent=self)
            return
        if not name:
            messagebox.showerror("Error", "El nombre es obligatorio.", parent=self)
            return
        # El nombre puede contener cualquier carácter, no se valida con regex
        if price <= 0:
            messagebox.showerror("Error", "El precio debe ser un número positivo mayor a cero.", parent=self)
            return
        if stock <= 0:
            messagebox.showerror("Error", "El stock debe ser un número positivo mayor a cero.", parent=self)
            return
        db.update_product(sku, name, price, stock)
        self.refresh_treeview()
        self.clear_form()

    def delete_item(self):
        selected = self.tree.selection()
        print("DEBUG selección delete:", selected)
        if not selected:
            messagebox.showerror("Error", "Seleccione un producto.", parent=self)
            return
        sku, name = self.tree.item(selected[0], "values")[0:2]
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{name}'?", parent=self):
            db.delete_product(sku)
            self.refresh_treeview()
            self.clear_form()

class UsersWindow(GenericCRUDWindow):
    def __init__(self, master):
        super().__init__(master, "Gestión de Usuarios", {"id": "ID", "username": "Usuario", "role": "Rol"}, {"Usuario": "text", "Contraseña": "text", "Rol": "combo"})
        self.refresh_treeview()
    def refresh_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for user in db.get_all_users():
            self.tree.insert("", "end", values=user)
    def populate_form(self, values):
        self.clear_form()
        self.entries['Usuario'].insert(0, values[1])
        self.entries['Rol'].set(values[2])
    def add_item(self):
        username = self.entries['Usuario'].get()
        password = self.entries['Contraseña'].get()
        role = self.entries['Rol'].get()
        if not all([username, password, role]):
            messagebox.showerror("Error", "Todos los campos son requeridos.", parent=self)
            return
        if db.add_user(username, password, role):
            self.refresh_treeview()
            self.clear_form()
        else:
            messagebox.showerror("Error", "El nombre de usuario ya existe.", parent=self)
    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Seleccione un usuario.", parent=self)
            return
        user_id, username, _ = self.tree.item(selected[0], "values")
        if username == 'admin':
            messagebox.showerror("Error", "No se puede eliminar al usuario 'admin'.", parent=self)
            return
        if messagebox.askyesno("Confirmar", f"¿Eliminar al usuario {username}?", parent=self):
            db.delete_user(user_id)
            self.refresh_treeview()
            self.clear_form()
    def update_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Seleccione un usuario.", parent=self)
            return
        user_id, username_old, _ = self.tree.item(selected[0], "values")
        if username_old == 'admin':
            messagebox.showerror("Error", "No se puede editar el usuario 'admin'.", parent=self)
            return
        username = self.entries['Usuario'].get()
        password = self.entries['Contraseña'].get()
        role = self.entries['Rol'].get()
        if not all([username, role]):
            messagebox.showerror("Error", "Usuario y Rol son requeridos.", parent=self)
            return
        if password:
            success = db.update_user(user_id, username, password, role)
        else:
            success = db.update_user(user_id, username, None, role)
        if success:
            self.refresh_treeview()
            self.clear_form()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el usuario. ¿El nombre ya existe?", parent=self)

class HistoryWindow(BaseTableWindow):
    def __init__(self, master):
        super().__init__(master, "Historial de Ventas")
        self.geometry("1000x600")

        tree_frame = tk.Frame(self, bg=COLOR_FRAME, padx=15, pady=15)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=15)
        columns = ("id", "user", "cliente", "cedula", "telefono", "total", "date")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        # Encabezados con sort
        for col, text in zip(columns, ["ID Venta", "Vendedor", "Cliente", "Cédula", "Teléfono", "Total", "Fecha y Hora"]):
            self.tree.heading(col, text=text, command=lambda _col=col: treeview_sort_column(self.tree, _col, False))
        self.tree.column("id", width=80)
        self.tree.column("user", width=120)
        self.tree.column("cliente", width=150)
        self.tree.column("cedula", width=100)
        self.tree.column("telefono", width=100)
        self.tree.column("total", width=100, anchor='e')
        self.tree.column("date", width=200)
        for sale in db.get_sales_history():
            self.tree.insert("", "end", values=(sale[0], sale[1], sale[4], sale[5], sale[6], f"${sale[2]:.2f}", sale[3]))
        self.tree.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()