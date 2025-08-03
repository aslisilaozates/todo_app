import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from tkinter import scrolledtext

class TodoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("To Do List Uygulamasi")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Veri dosyası
        self.tasks_file = "tasks.json"
        self.tasks = self.load_tasks()
        
        # Ana stil
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
        self.refresh_task_list()
    
    def load_tasks(self):
        """JSON dosyasından görevleri yükle"""
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                messagebox.showerror("Hata", "Görev dosyası bozuk. Yeni dosya oluşturuluyor.")
                return []
        return []
    
    def save_tasks(self):
        """Görevleri JSON dosyasına kaydet"""
        try:
            with open(self.tasks_file, 'w', encoding='utf-8') as file:
                json.dump(self.tasks, file, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Hata", f"Görevler kaydedilemedi: {e}")
    
    def create_widgets(self):
        """Widget'ları oluştur"""
        # Ana frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Başlık
        title_label = ttk.Label(main_frame, text="TO DO LIST UYGULAMASI", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Sol panel - Görev ekleme
        left_frame = ttk.LabelFrame(main_frame, text="Yeni Görev Ekle", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Başlık
        ttk.Label(left_frame, text="Başlık:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_entry = ttk.Entry(left_frame, width=30)
        self.title_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Açıklama
        ttk.Label(left_frame, text="Açıklama:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.description_text = scrolledtext.ScrolledText(left_frame, width=30, height=4)
        self.description_text.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Öncelik
        ttk.Label(left_frame, text="Öncelik:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.priority_var = tk.StringVar(value="orta")
        priority_combo = ttk.Combobox(left_frame, textvariable=self.priority_var, 
                                     values=["düşük", "orta", "yüksek"], state="readonly")
        priority_combo.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Ekle butonu
        add_button = ttk.Button(left_frame, text="Görev Ekle", command=self.add_task)
        add_button.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Sağ panel - Görev listesi
        right_frame = ttk.LabelFrame(main_frame, text="Görevler", padding="10")
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Filtre
        filter_frame = ttk.Frame(right_frame)
        filter_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(filter_frame, text="Filtre:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="tümü")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                   values=["tümü", "bekliyor", "tamamlandı"], 
                                   state="readonly", width=15)
        filter_combo.pack(side=tk.LEFT, padx=(5, 0))
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_task_list())
        
        # Görev listesi
        self.task_tree = ttk.Treeview(right_frame, columns=("id", "title", "priority", "status"), 
                                     show="headings", height=15)
        self.task_tree.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        scrollbar.grid(row=1, column=3, sticky=(tk.N, tk.S))
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        # Sütun başlıkları
        self.task_tree.heading("id", text="ID")
        self.task_tree.heading("title", text="Başlık")
        self.task_tree.heading("priority", text="Öncelik")
        self.task_tree.heading("status", text="Durum")
        
        # Sütun genişlikleri
        self.task_tree.column("id", width=50)
        self.task_tree.column("title", width=200)
        self.task_tree.column("priority", width=80)
        self.task_tree.column("status", width=100)
        
        # Butonlar
        button_frame = ttk.Frame(right_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Tamamla", command=self.complete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Düzenle", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Sil", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="İstatistikler", command=self.show_statistics).pack(side=tk.LEFT, padx=5)
        
        # Grid ağırlıkları
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
    
    def add_task(self):
        """Yeni görev ekle"""
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Hata", "Başlık boş olamaz!")
            return
        
        description = self.description_text.get("1.0", tk.END).strip()
        priority = self.priority_var.get()
        
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "priority": priority,
            "status": "bekliyor",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "completed_at": None
        }
        
        self.tasks.append(task)
        self.save_tasks()
        self.refresh_task_list()
        
        # Formu temizle
        self.title_entry.delete(0, tk.END)
        self.description_text.delete("1.0", tk.END)
        self.priority_var.set("orta")
        
        messagebox.showinfo("Başarılı", f"Görev eklendi: {title}")
    
    def refresh_task_list(self):
        """Görev listesini yenile"""
        # Mevcut öğeleri temizle
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Filtre uygula
        filter_value = self.filter_var.get()
        filtered_tasks = self.tasks
        if filter_value != "tümü":
            filtered_tasks = [task for task in self.tasks if task["status"] == filter_value]
        
        # Görevleri listele
        for task in filtered_tasks:
            self.task_tree.insert("", "end", values=(
                task["id"],
                task["title"],
                task["priority"],
                task["status"]
            ))
    
    def complete_task(self):
        """Görevi tamamla"""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen bir görev seçin!")
            return
        
        item = self.task_tree.item(selected[0])
        task_id = item['values'][0]
        
        for task in self.tasks:
            if task["id"] == task_id:
                if task["status"] == "tamamlandı":
                    messagebox.showinfo("Bilgi", f"Görev zaten tamamlanmış: {task['title']}")
                    return
                
                task["status"] = "tamamlandı"
                task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_tasks()
                self.refresh_task_list()
                messagebox.showinfo("Başarılı", f"Görev tamamlandı: {task['title']}")
                return
        
        messagebox.showerror("Hata", f"Görev bulunamadı: ID {task_id}")
    
    def delete_task(self):
        """Görevi sil"""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen bir görev seçin!")
            return
        
        item = self.task_tree.item(selected[0])
        task_id = item['values'][0]
        task_title = item['values'][1]
        
        if messagebox.askyesno("Onay", f"Bu görevi silmek istediğinizden emin misiniz?\n\n{task_title}"):
            for i, task in enumerate(self.tasks):
                if task["id"] == task_id:
                    deleted_task = self.tasks.pop(i)
                    self.save_tasks()
                    self.refresh_task_list()
                    messagebox.showinfo("Başarılı", f"Görev silindi: {deleted_task['title']}")
                    return
            
            messagebox.showerror("Hata", f"Görev bulunamadı: ID {task_id}")
    
    def edit_task(self):
        """Görevi düzenle"""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen bir görev seçin!")
            return
        
        item = self.task_tree.item(selected[0])
        task_id = item['values'][0]
        
        # Görevi bul
        task = None
        for t in self.tasks:
            if t["id"] == task_id:
                task = t
                break
        
        if not task:
            messagebox.showerror("Hata", f"Görev bulunamadı: ID {task_id}")
            return
        
        # Düzenleme penceresi
        self.create_edit_window(task)
    
    def create_edit_window(self, task):
        """Düzenleme penceresi oluştur"""
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Görev Düzenle")
        edit_window.geometry("400x300")
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Widget'lar
        ttk.Label(edit_window, text="Başlık:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        title_entry = ttk.Entry(edit_window, width=40)
        title_entry.insert(0, task["title"])
        title_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        ttk.Label(edit_window, text="Açıklama:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        desc_text = scrolledtext.ScrolledText(edit_window, width=40, height=6)
        desc_text.insert("1.0", task["description"])
        desc_text.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        ttk.Label(edit_window, text="Öncelik:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        priority_var = tk.StringVar(value=task["priority"])
        priority_combo = ttk.Combobox(edit_window, textvariable=priority_var, 
                                     values=["düşük", "orta", "yüksek"], state="readonly")
        priority_combo.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        # Butonlar
        button_frame = ttk.Frame(edit_window)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        def save_changes():
            task["title"] = title_entry.get().strip()
            task["description"] = desc_text.get("1.0", tk.END).strip()
            task["priority"] = priority_var.get()
            
            self.save_tasks()
            self.refresh_task_list()
            edit_window.destroy()
            messagebox.showinfo("Başarılı", "Görev güncellendi!")
        
        ttk.Button(button_frame, text="Kaydet", command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="İptal", command=edit_window.destroy).pack(side=tk.LEFT, padx=5)
        
        edit_window.columnconfigure(0, weight=1)
    
    def show_statistics(self):
        """İstatistikleri göster"""
        total = len(self.tasks)
        completed = len([task for task in self.tasks if task["status"] == "tamamlandı"])
        pending = total - completed
        
        # Öncelik dağılımı
        priorities = {}
        for task in self.tasks:
            priority = task["priority"]
            priorities[priority] = priorities.get(priority, 0) + 1
        
        stats_text = f"""
İSTATİSTİKLER
{'='*30}

Toplam Görev: {total}
Tamamlanan: {completed}
Bekleyen: {pending}

"""
        
        if total > 0:
            completion_rate = (completed / total) * 100
            stats_text += f"Tamamlanma Oranı: %{completion_rate:.1f}\n\n"
        
        if priorities:
            stats_text += "Öncelik Dağılımı:\n"
            for priority, count in priorities.items():
                stats_text += f"  {priority}: {count} görev\n"
        
        messagebox.showinfo("İstatistikler", stats_text)

def main():
    root = tk.Tk()
    app = TodoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 