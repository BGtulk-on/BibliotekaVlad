from abc import ABC, abstractmethod
import json

class Book(ABC):
    def __init__(self, title, author, year, genre):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
    
    @abstractmethod
    def get_info(self):
        pass
    
    def __str__(self):
        return self.get_info()

class FictionBook(Book):
    def __init__(self, title, author, year, genre, style):
        super().__init__(title, author, year, genre)
        self.style = style
    
    def get_info(self):
        return f"Художествена книга: '{self.title}' от {self.author} ({self.year}), жанр: {self.genre}, стил: {self.style}"

class AcademicBook(Book):
    def __init__(self, title, author, year, genre, field, university):
        super().__init__(title, author, year, genre)
        self.field = field
        self.university = university
    
    def get_info(self):
        return f"Научна книга: '{self.title}' от {self.author} ({self.year}), област: {self.field}, университет: {self.university}"

class Magazine(Book):
    def __init__(self, title, author, year, genre, issue_number, month):
        super().__init__(title, author, year, genre)
        self.issue_number = issue_number
        self.month = month
    
    def get_info(self):
        return f"Списание: '{self.title}' от {self.author} ({self.year}), брой: {self.issue_number}, месец: {self.month}"

class BookFactory:
    @staticmethod
    def create_book(book_type, **kwargs):
        if book_type == "fiction":
            return FictionBook(
                kwargs['title'], 
                kwargs['author'], 
                kwargs['year'], 
                kwargs['genre'], 
                kwargs['style']
            )
        elif book_type == "academic":
            return AcademicBook(
                kwargs['title'], 
                kwargs['author'], 
                kwargs['year'], 
                kwargs['genre'], 
                kwargs['field'], 
                kwargs['university']
            )
        elif book_type == "magazine":
            return Magazine(
                kwargs['title'], 
                kwargs['author'], 
                kwargs['year'], 
                kwargs['genre'], 
                kwargs['issue_number'], 
                kwargs['month']
            )
        else:
            raise ValueError(f"Непознат тип книга: {book_type}")


class BookBuilder(ABC):
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.title = ""
        self.author = ""
        self.year = 0
        self.genre = ""
    
    def set_title(self, title):
        self.title = title
        return self
    
    def set_author(self, author):
        self.author = author
        return self
    
    def set_year(self, year):
        self.year = year
        return self
    
    def set_genre(self, genre):
        self.genre = genre
        return self
    
    @abstractmethod
    def build(self):
        pass

class FictionBookBuilder(BookBuilder):
    def reset(self):
        super().reset()
        self.style = ""
    
    def set_style(self, style):
        self.style = style
        return self
    
    def build(self):
        return FictionBook(self.title, self.author, self.year, self.genre, self.style)

class AcademicBookBuilder(BookBuilder):
    def reset(self):
        super().reset()
        self.field = ""
        self.university = ""
    
    def set_field(self, field):
        self.field = field
        return self
    
    def set_university(self, university):
        self.university = university
        return self
    
    def build(self):
        return AcademicBook(self.title, self.author, self.year, self.genre, self.field, self.university)

class MagazineBuilder(BookBuilder):
    def reset(self):
        super().reset()
        self.issue_number = 0
        self.month = ""
    
    def set_issue_number(self, issue_number):
        self.issue_number = issue_number
        return self
    
    def set_month(self, month):
        self.month = month
        return self
    
    def build(self):
        return Magazine(self.title, self.author, self.year, self.genre, self.issue_number, self.month)

class BookDirector:
    def __init__(self, builder):
        self.builder = builder
    
    def make_simple_fiction_book(self, title, author):
        return (self.builder
                .reset()
                .set_title(title)
                .set_author(author)
                .set_year(2024)
                .set_genre("приключения")
                .set_style("фентъзи")
                .build())
    
    def make_academic_book(self, title, author, field, university):
        return (self.builder
                .reset()
                .set_title(title)
                .set_author(author)
                .set_year(2024)
                .set_genre("наука")
                .set_field(field)
                .set_university(university)
                .build())


class Library:
    def __init__(self):
        self.books = []
    
    def add_book(self, book):
        self.books.append(book)
        print(f"Добавена книга: {book.title}")
    
    def show_all_books(self):
        if not self.books:
            print("Библиотеката е празна!")
            return
        
        print("\n=== ВСИЧКИ КНИГИ В БИБЛИОТЕКАТА ===")
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book.get_info()}")
    
    def search_by_author(self, author):
        found = [book for book in self.books if author.lower() in book.author.lower()]
        if found:
            print(f"\nКниги от автор '{author}':")
            for book in found:
                print(f"- {book.get_info()}")
        else:
            print(f"Няма книги от автор '{author}'")
    
    def search_by_genre(self, genre):
        found = [book for book in self.books if genre.lower() in book.genre.lower()]
        if found:
            print(f"\nКниги от жанр '{genre}':")
            for book in found:
                print(f"- {book.get_info()}")
        else:
            print(f"Няма книги от жанр '{genre}'")
    
    def search_by_title(self, title):
        found = [book for book in self.books if title.lower() in book.title.lower()]
        if found:
            print(f"\nКниги със заглавие съдържащо '{title}':")
            for book in found:
                print(f"- {book.get_info()}")
        else:
            print(f"Няма книги със заглавие съдържащо '{title}'")
    
    def remove_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                self.books.remove(book)
                print(f"Премахната книга: {title}")
                return
        print(f"Няма книга с точно заглавие '{title}'")
    
    def sort_books_by_year(self):
        self.books.sort(key=lambda x: x.year)
        print("Книгите са сортирани по година.")
    
    def save_to_file(self, filename):
        try:
            data = []
            for book in self.books:
                book_data = {
                    'type': book.__class__.__name__,
                    'title': book.title,
                    'author': book.author,
                    'year': book.year,
                    'genre': book.genre
                }
                
                if isinstance(book, FictionBook):
                    book_data['style'] = book.style
                elif isinstance(book, AcademicBook):
                    book_data['field'] = book.field
                    book_data['university'] = book.university
                elif isinstance(book, Magazine):
                    book_data['issue_number'] = book.issue_number
                    book_data['month'] = book.month
                
                data.append(book_data)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Каталогът е записан в файл {filename}")
        except Exception as e:
            print(f"Грешка при записване: {e}")
    
    def load_from_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.books = []
            for book_data in data:
                if book_data['type'] == 'FictionBook':
                    book = FictionBook(
                        book_data['title'],
                        book_data['author'],
                        book_data['year'],
                        book_data['genre'],
                        book_data['style']
                    )
                elif book_data['type'] == 'AcademicBook':
                    book = AcademicBook(
                        book_data['title'],
                        book_data['author'],
                        book_data['year'],
                        book_data['genre'],
                        book_data['field'],
                        book_data['university']
                    )
                elif book_data['type'] == 'Magazine':
                    book = Magazine(
                        book_data['title'],
                        book_data['author'],
                        book_data['year'],
                        book_data['genre'],
                        book_data['issue_number'],
                        book_data['month']
                    )
                
                self.books.append(book)
            
            print(f"Каталогът е зареден от файл {filename}")
        except FileNotFoundError:
            print(f"Файлът {filename} не съществува")
        except Exception as e:
            print(f"Грешка при зареждане: {e}")

def show_menu():
    print("\n" + "="*50)
    print("  ____   ____ _         _ _    ")
    print(" | __ ) / ___| |_ _   _| | | __")
    print(" |  _ \\| |  _| __| | | | | |/ /")
    print(" | |_) | |_| | |_| |_| | |   < ")
    print(" |____/ \\____\\\\__|\\__,_|_|_|\\_\\")
    print("")
    print("📚 СИСТЕМА ЗА УПРАВЛЕНИЕ НА БИБЛИОТЕКА 📚")
    print("="*50)
    print("1. Добави книга чрез Factory")
    print("2. Добави книга чрез Builder")
    print("3. Покажи всички книги")
    print("4. Търси по автор")
    print("5. Търси по жанр")
    print("6. Търси по заглавие")
    print("7. Премахни книга")
    print("8. Сортирай по година")
    print("9. Запази в файл")
    print("10. Зареди от файл")
    print("0. Изход")

def main():
    library = Library()
    
    while True:
        show_menu()
        choice = input("\nВашият избор: ")
        
        if choice == "1":
            print("\nВидове книги: fiction, academic, magazine")
            book_type = input("Въведете тип книга: ")
            
            title = input("Заглавие: ")
            author = input("Автор: ")
            year = int(input("Година: "))
            genre = input("Жанр: ")
            
            try:
                if book_type == "fiction":
                    style = input("Стил: ")
                    book = BookFactory.create_book(book_type, 
                                                  title=title, author=author, 
                                                  year=year, genre=genre, style=style)
                elif book_type == "academic":
                    field = input("Научна област: ")
                    university = input("Университет: ")
                    book = BookFactory.create_book(book_type, 
                                                  title=title, author=author, 
                                                  year=year, genre=genre, 
                                                  field=field, university=university)
                elif book_type == "magazine":
                    issue_number = int(input("Номер на издание: "))
                    month = input("Месец: ")
                    book = BookFactory.create_book(book_type, 
                                                  title=title, author=author, 
                                                  year=year, genre=genre, 
                                                  issue_number=issue_number, month=month)
                
                library.add_book(book)
            except Exception as e:
                print(f"Грешка: {e}")
        
        elif choice == "2":
            print("\nВидове builders: 1-Fiction, 2-Academic, 3-Magazine")
            builder_choice = input("Избор: ")
            
            if builder_choice == "1":
                builder = FictionBookBuilder()
                director = BookDirector(builder)
                title = input("Заглавие: ")
                author = input("Автор: ")
                book = director.make_simple_fiction_book(title, author)
                library.add_book(book)
            
            elif builder_choice == "2":
                builder = AcademicBookBuilder()
                director = BookDirector(builder)
                title = input("Заглавие: ")
                author = input("Автор: ")
                field = input("Научна област: ")
                university = input("Университет: ")
                book = director.make_academic_book(title, author, field, university)
                library.add_book(book)
            
            elif builder_choice == "3":
                builder = MagazineBuilder()
                title = input("Заглавие: ")
                author = input("Автор: ")
                year = int(input("Година: "))
                issue = int(input("Номер: "))
                month = input("Месец: ")
                
                book = (builder.set_title(title)
                             .set_author(author)
                             .set_year(year)
                             .set_genre("списание")
                             .set_issue_number(issue)
                             .set_month(month)
                             .build())
                library.add_book(book)
        
        elif choice == "3":
            library.show_all_books()
        
        elif choice == "4":
            author = input("Въведете автор за търсене: ")
            library.search_by_author(author)
        
        elif choice == "5":
            genre = input("Въведете жанр за търсене: ")
            library.search_by_genre(genre)
        
        elif choice == "6":
            title = input("Въведете заглавие за търсене: ")
            library.search_by_title(title)
        
        elif choice == "7":
            title = input("Въведете точното заглавие за премахване: ")
            library.remove_book(title)
        
        elif choice == "8":
            library.sort_books_by_year()
        
        elif choice == "9":
            filename = input("Име на файл (напр. library.json): ")
            library.save_to_file(filename)
        
        elif choice == "10":
            filename = input("Име на файл за зареждане: ")
            library.load_from_file(filename)
        
        elif choice == "0":
            print("Довиждане!")
            break
        
        else:
            print("Невалиден избор!")

def demo():
    print("=== ДЕМОНСТРАЦИЯ НА СИСТЕМАТА ===")
    library = Library()
    
    print("\n1. Създаване на книги чрез Factory:")
    
    fiction_book = BookFactory.create_book("fiction", 
                                          title="Властелинът на пръстените", 
                                          author="Толкин", 
                                          year=1954, 
                                          genre="фентъзи", 
                                          style="епическо фентъзи")
    library.add_book(fiction_book)
    
    academic_book = BookFactory.create_book("academic", 
                                           title="Програмиране с Python", 
                                           author="Иван Петров", 
                                           year=2023, 
                                           genre="информатика", 
                                           field="Компютърни науки", 
                                           university="СУ")
    library.add_book(academic_book)
    
    print("\n2. Създаване на книги чрез Builder:")
    
    fiction_builder = FictionBookBuilder()
    fiction_book2 = (fiction_builder.set_title("Хари Потър")
                                   .set_author("Роулинг")
                                   .set_year(1997)
                                   .set_genre("фентъзи")
                                   .set_style("магическо фентъзи")
                                   .build())
    library.add_book(fiction_book2)
    library.show_all_books()
    print("\n3. Търсене по автор:")
    library.search_by_author("Толкин")
    print("\n4. Премахване на книга:")
    library.remove_book("Програмиране с Python")
    
    library.show_all_books()

if __name__ == "__main__":
    print("Изберете режим:")
    print("1. Демонстрация")
    print("2. Интерактивно меню")
    
    mode = input("Вашият избор: ")
    
    if mode == "1":
        demo()
    else:
        main()