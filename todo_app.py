import json
import os
from datetime import datetime
import sys
import codecs

class TodoApp:
    def __init__(self):
        self.tasks_file = "tasks.json"
        self.tasks = self.load_tasks()
        
    def load_tasks(self):
        """JSON dosyasından görevleri yükle"""
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("❌ Görev dosyası bozuk. Yeni dosya oluşturuluyor...")
                return []
        return []
    
    def save_tasks(self):
        """Görevleri JSON dosyasına kaydet"""
        try:
            with open(self.tasks_file, 'w', encoding='utf-8') as file:
                json.dump(self.tasks, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Görevler kaydedilemedi: {e}")
    
    def add_task(self, title, description="", priority="orta"):
        """Yeni görev ekle"""
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
        print(f"Gorev eklendi: {title}")
    
    def list_tasks(self, status_filter=None):
        """Görevleri listele"""
        if not self.tasks:
            print("Henuz gorev bulunmuyor.")
            return
        
        filtered_tasks = self.tasks
        if status_filter:
            filtered_tasks = [task for task in self.tasks if task["status"] == status_filter]
        
        if not filtered_tasks:
            print(f"{status_filter} durumunda gorev bulunamadi.")
            return
        
        print(f"\nGorevler ({len(filtered_tasks)} adet):")
        print("-" * 80)
        
        for task in filtered_tasks:
            status_icon = "[TAMAMLANDI]" if task["status"] == "tamamlandı" else "[BEKLIYOR]"
            priority_icon = {
                "düşük": "[DUSUK]",
                "orta": "[ORTA]", 
                "yüksek": "[YUKSEK]"
            }.get(task["priority"], "[ORTA]")
            
            print(f"{status_icon} {priority_icon} {task['id']}. {task['title']}")
            if task['description']:
                print(f"   Aciklama: {task['description']}")
            print(f"   Olusturulma: {task['created_at']}")
            if task['completed_at']:
                print(f"   Tamamlanma: {task['completed_at']}")
            print()
    
    def complete_task(self, task_id):
        """Görevi tamamla"""
        for task in self.tasks:
            if task["id"] == task_id:
                if task["status"] == "tamamlandı":
                    print(f"Gorev zaten tamamlanmis: {task['title']}")
                    return
                
                task["status"] = "tamamlandı"
                task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_tasks()
                print(f"Gorev tamamlandi: {task['title']}")
                return
        
        print(f"Gorev bulunamadi: ID {task_id}")
    
    def delete_task(self, task_id):
        """Görevi sil"""
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                deleted_task = self.tasks.pop(i)
                self.save_tasks()
                print(f"Gorev silindi: {deleted_task['title']}")
                return
        
        print(f"Gorev bulunamadi: ID {task_id}")
    
    def edit_task(self, task_id, new_title=None, new_description=None, new_priority=None):
        """Görevi düzenle"""
        for task in self.tasks:
            if task["id"] == task_id:
                if new_title:
                    task["title"] = new_title
                if new_description:
                    task["description"] = new_description
                if new_priority:
                    task["priority"] = new_priority
                
                self.save_tasks()
                print(f"Gorev guncellendi: {task['title']}")
                return
        
        print(f"Gorev bulunamadi: ID {task_id}")
    
    def get_statistics(self):
        """İstatistikleri göster"""
        total = len(self.tasks)
        completed = len([task for task in self.tasks if task["status"] == "tamamlandı"])
        pending = total - completed
        
        print("\nIstatistikler:")
        print("-" * 30)
        print(f"Toplam gorev: {total}")
        print(f"Tamamlanan: {completed}")
        print(f"Bekleyen: {pending}")
        
        if total > 0:
            completion_rate = (completed / total) * 100
            print(f"Tamamlanma orani: %{completion_rate:.1f}")
        
        # Öncelik dağılımı
        priorities = {}
        for task in self.tasks:
            priority = task["priority"]
            priorities[priority] = priorities.get(priority, 0) + 1
        
        if priorities:
            print("\nOncelik dagilimi:")
            for priority, count in priorities.items():
                print(f"   {priority}: {count} gorev")
    
    def show_menu(self):
        """Ana menüyü göster"""
        print("\n" + "="*50)
        print("TO DO LIST UYGULAMASI")
        print("="*50)
        print("1. Yeni gorev ekle")
        print("2. Tum gorevleri listele")
        print("3. Bekleyen gorevleri listele")
        print("4. Tamamlanan gorevleri listele")
        print("5. Gorev tamamla")
        print("6. Gorev sil")
        print("7. Gorev duzenle")
        print("8. Istatistikler")
        print("9. Cikis")
        print("="*50)
    
    def run(self):
        """Uygulamayı çalıştır"""
        print("To Do List uygulamasina hos geldiniz!")
        
        while True:
            self.show_menu()
            choice = input("\nSeçiminizi yapın (1-9): ").strip()
            
            if choice == "1":
                title = input("Gorev basligi: ").strip()
                if not title:
                    print("Baslik bos olamaz!")
                    continue
                
                description = input("Aciklama (opsiyonel): ").strip()
                priority = input("Oncelik (dusuk/orta/yuksek) [orta]: ").strip().lower()
                if priority not in ["düşük", "orta", "yüksek"]:
                    priority = "orta"
                
                self.add_task(title, description, priority)
                
            elif choice == "2":
                self.list_tasks()
                
            elif choice == "3":
                self.list_tasks("bekliyor")
                
            elif choice == "4":
                self.list_tasks("tamamlandı")
                
            elif choice == "5":
                try:
                    task_id = int(input("Tamamlanacak gorevin ID'si: "))
                    self.complete_task(task_id)
                except ValueError:
                    print("Gecersiz ID!")
                
            elif choice == "6":
                try:
                    task_id = int(input("Silinecek gorevin ID'si: "))
                    confirm = input("Bu gorevi silmek istediginizden emin misiniz? (e/h): ").strip().lower()
                    if confirm in ["e", "evet", "y", "yes"]:
                        self.delete_task(task_id)
                except ValueError:
                    print("Gecersiz ID!")
                
            elif choice == "7":
                try:
                    task_id = int(input("Duzenlenecek gorevin ID'si: "))
                    new_title = input("Yeni baslik (degistirmek istemiyorsaniz bos birakin): ").strip()
                    new_description = input("Yeni aciklama (degistirmek istemiyorsaniz bos birakin): ").strip()
                    new_priority = input("Yeni oncelik (dusuk/orta/yuksek) (degistirmek istemiyorsaniz bos birakin): ").strip().lower()
                    
                    if new_priority and new_priority not in ["düşük", "orta", "yüksek"]:
                        print("Gecersiz oncelik!")
                        continue
                    
                    self.edit_task(task_id, new_title or None, new_description or None, new_priority or None)
                except ValueError:
                    print("Gecersiz ID!")
                
            elif choice == "8":
                self.get_statistics()
                
            elif choice == "9":
                print("Gorusuruz!")
                break
                
            else:
                print("Gecersiz secim! Lutfen 1-9 arasi bir sayi girin.")
            
            input("\nDevam etmek için Enter'a basın...")

if __name__ == "__main__":
    app = TodoApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nUygulama kapatiliyor...")
        sys.exit(0) 