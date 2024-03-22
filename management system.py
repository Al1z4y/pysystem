import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # You need to install the Pillow library for this
from pathlib import Path


import json
# File to store user data
USER_FILE = "users.json"
{
  "uzair": {
    "password": "meow",
    "movies": []
  },

  "admin": {
    "password": "adminpassword",
    "role": "admin" 
  }
}

# File to store movie data
MOVIE_FILE = "movies.json"
RATINGS_FILE = "ratings.json"
REVIEWS_FILE = "reviews.json"

class MovieManagementSystem:
    RATINGS_FILE = "ratings.json"
    REVIEWS_FILE = "reviews.json"
   
    
    def __init__(self, root):
      
        self.root = root
        self.root.title("Movie Management System")
        self.root.geometry("600x400")

        # Load users from file
        self.users = self.load_users()

        self.current_user = None
        self.movies = self.load_movies()
        self.ratings, self.reviews = self.load_ratings_and_reviews()
        self.root = root
        self.movies = []  # Your movie data
        self.users = {}   # Your user data
        self.logged_in_user = None  # Attribute to track the logged-in user
        self.text_movies = None  # Initialize text_movies attribute

      

        

        # Initialize text_movies in the __init__ method
        self.text_movies = None
        

        # Set the background image
        image_path = str(Path.home() / 'Downloads' / 'meow.png')
        self.background_image = ImageTk.PhotoImage(Image.open(image_path))
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.text_movies = None  # Add this line to initialize text_movies attribute

        self.role_selection_screen()

    # ... (rest of your code)



    # ... (your existing imports and class definition)



    def admin_menu(self):
        admin_frame = tk.Frame(self.root)
        admin_frame.pack(pady=20)

        add_movie_button = tk.Button(admin_frame, text="Add Movie", command=self.add_movie_screen)
        view_movies_button = tk.Button(admin_frame, text="View Movies", command=self.view_movies_screen)
        view_ratings_button = tk.Button(admin_frame, text="View Ratings", command=self.view_ratings_screen)
        search_filter_button = tk.Button(admin_frame, text="Search and Filter", command=self.search_and_filter_screen)
        logout_button = tk.Button(admin_frame, text="Logout", command=self.logout)

        add_movie_button.grid(row=0, column=0, pady=10)
        view_movies_button.grid(row=1, column=0, pady=10)
        view_ratings_button.grid(row=2, column=0, pady=10)
        search_filter_button.grid(row=3, column=0, pady=10)
        logout_button.grid(row=4, column=0, pady=10)

    def delete_movie_screen(self):
        delete_movie_window = tk.Toplevel(self.root)
        delete_movie_window.title("Delete Movie")

        label_title = tk.Label(delete_movie_window, text="Title:")
        entry_title = tk.Entry(delete_movie_window)

        label_title.grid(row=0, column=0)
        entry_title.grid(row=0, column=1)

        delete_button = tk.Button(delete_movie_window, text="Delete", command=lambda: self.delete_movie(entry_title.get()))
        delete_button.grid(row=1, column=0, columnspan=2, pady=10)

    def delete_movie(self, title):
        for i, movie in enumerate(self.movies):
            if movie["Title"].lower() == title.lower():
                del self.movies[i]
                self.save_data()
                messagebox.showinfo("Success", f"Movie '{title}' deleted successfully!")
                return

        messagebox.showerror("Error", f"Movie '{title}' not found.")
    def edit_movie_screen(self):
        edit_movie_window = tk.Toplevel(self.root)
        edit_movie_window.title("Edit Movie")

        label_title = tk.Label(edit_movie_window, text="Title:")
        entry_title = tk.Entry(edit_movie_window)
        label_field = tk.Label(edit_movie_window, text="Field to Edit:")
        entry_field = tk.Entry(edit_movie_window)
        label_new_value = tk.Label(edit_movie_window, text="New Value:")
        entry_new_value = tk.Entry(edit_movie_window)

        label_title.grid(row=0, column=0)
        entry_title.grid(row=0, column=1)
        label_field.grid(row=1, column=0)
        entry_field.grid(row=1, column=1)
        label_new_value.grid(row=2, column=0)
        entry_new_value.grid(row=2, column=1)

        edit_button = tk.Button(edit_movie_window, text="Edit", command=lambda: self.edit_movie(entry_title.get(), entry_field.get(), entry_new_value.get()))
        edit_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Do NOT call display_movies here; it should be called in view_movies_screen or wherever appropriate



    def edit_movie(self, title, field, new_value):
        for i, movie in enumerate(self.movies):
            if movie["Title"].lower() == title.lower():
                if field.lower() in map(str.lower, movie.keys()):
                    if field.lower() == "year" and not new_value.isdigit():
                        messagebox.showerror("Error", "Year must be a valid number.")
                        return

                    movie[field] = new_value

                    # Check if text_movies is initialized before using it
                    if self.text_movies:
                        self.text_movies.delete(1.0, tk.END)
                        self.refresh_view_movies()

                    # Update movies in self.users dictionary
                    if self.current_user in self.users:
                        self.users[self.current_user]["movies"] = self.movies

                    self.save_data()
                    messagebox.showinfo("Success", f"Movie '{title}' edited successfully!")
                    return

        messagebox.showerror("Error", f"Movie '{title}' not found or field '{field}' does not exist.")
    def view_movies_screen(self):
        self.view_movies_window = tk.Toplevel(self.root)
        self.view_movies_window.title("View Movies")

        self.text_movies = tk.Text(self.view_movies_window, height=10, width=50)
        self.text_movies.pack(pady=20)

        self.refresh_view_movies()  # Add this line to display movies initially

    def refresh_view_movies(self):
        if not hasattr(self, 'text_movies') or not self.text_movies.winfo_exists():
            return

        # Clear the existing content in the Text widget
        self.text_movies.delete(1.0, tk.END)

        # Display the updated movie list
        for i, movie in enumerate(self.movies):
            self.text_movies.insert(tk.END, f"{i + 1}. Title: {movie['Title']}\nYear: {movie['Year']}\nGenre: {movie['Genre']}\nDirector: {movie['Director']}\nCast: {movie['Cast']}\n")
            self.text_movies.insert(tk.END, f"Rating: {self.get_movie_rating(i)}\n")
            self.text_movies.insert(tk.END, f"Review: {self.get_movie_review(i)}\n\n")


    def display_movies(self):
        if self.text_movies is not None:
            self.text_movies.destroy()  # Destroy the existing Text widget if it exists

        self.text_movies = tk.Text(self.root, wrap=tk.WORD, width=50, height=20)
        self.text_movies.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        for movie in self.movies:
            self.text_movies.insert(tk.END, f"{movie}\n\n")

        self.text_movies.config(state=tk.DISABLED)  # Disable editing of th



# ... (rest of your code)




    def forgot_password_screen(self):
        forgot_password_window = tk.Toplevel(self.root)
        forgot_password_window.title("Forgot Password")

        label_username = tk.Label(forgot_password_window, text="Username:")
        entry_username = tk.Entry(forgot_password_window)
        label_username.grid(row=0, column=0)
        entry_username.grid(row=0, column=1)

        recover_button = tk.Button(forgot_password_window, text="Recover Password", command=lambda: self.display_new_password_entry(entry_username.get(), forgot_password_window))
        recover_button.grid(row=1, column=0, columnspan=2, pady=10)

    def display_new_password_entry(self, username, window):
        if username in self.users:
            window.destroy()  # Close the current window
            new_password_window = tk.Toplevel(self.root)
            new_password_window.title("New Password")

            label_new_password = tk.Label(new_password_window, text="New Password:")
            entry_new_password = tk.Entry(new_password_window, show="*")
            label_new_password.grid(row=0, column=0)
            entry_new_password.grid(row=0, column=1)

            update_password_button = tk.Button(new_password_window, text="Update Password", command=lambda: self.recover_password(username, entry_new_password.get(), new_password_window))
            update_password_button.grid(row=1, column=0, columnspan=2, pady=10)
        else:
            messagebox.showerror("Error", "Invalid username. Please enter a valid username.")

    def recover_password(self, username, new_password, window):
        self.users[username]["password"] = new_password
        self.save_data()
        window.destroy()  # Close the current window
        messagebox.showinfo("Password Recovered", "Password has been updated successfully.")




    def load_users(self):
        try:
            with open(USER_FILE, "r") as file:
                users = json.load(file)
                # Check if "uzair" is not present and add the user with the "role" field
                if "uzair" not in users:
                    users["uzair"] = {"password": "meow", "role": "user"}  # Change role to "user"
                return users
        except FileNotFoundError:
            return {"uzair": {"password": "meow", "role": "user"}}  # Change role to "user"


        

    def load_ratings_and_reviews(self):
        try:
            with open(MovieManagementSystem.RATINGS_FILE, "r") as ratings_file, open(MovieManagementSystem.REVIEWS_FILE, "r") as reviews_file:
                ratings = json.load(ratings_file)
                reviews = json.load(reviews_file)
                return ratings, reviews
        except FileNotFoundError:
            return {}, {}

    def save_ratings_and_reviews(self):
        with open(MovieManagementSystem.RATINGS_FILE, "w") as ratings_file, open(MovieManagementSystem.REVIEWS_FILE, "w") as reviews_file:
            json.dump(self.ratings, ratings_file, indent=2)
            json.dump(self.reviews, reviews_file, indent=2)


    def save_data(self):
        # Save users to file
        with open(USER_FILE, "w") as file:
            json.dump(self.users, file, indent=2)

        # Save movies specific to the current user
        if self.current_user in self.users:
            self.users[self.current_user]["movies"] = self.movies
            with open(MOVIE_FILE, "w") as movie_file:
                json.dump(self.movies, movie_file, indent=2)

        # Save ratings and reviews
        self.save_ratings_and_reviews()

    

    def load_movies(self):
        # Load movies specific to the current user
        if self.current_user in self.users:
            user_data = self.users[self.current_user]
            if "movies" in user_data:
                return user_data["movies"]
        return []

    def role_selection_screen(self):
        role_frame = tk.Frame(self.root)
        role_frame.pack(pady=50)

        user_button = tk.Button(role_frame, text="User", command=lambda: self.show_login_screen("user"))
        admin_button = tk.Button(role_frame, text="Admin", command=lambda: self.show_login_screen("admin"))

        user_button.grid(row=0, column=0, pady=10)
        admin_button.grid(row=0, column=1, pady=10)

    def show_login_screen(self, role):
        # Destroy the existing role selection screen
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Movie Management System")
        self.root.geometry("600x400")

        # Load users from file
        self.users = self.load_users()

        # Set the background image
        image_path = str(Path.home() / 'Downloads' / 'meow.png')
        self.background_image = ImageTk.PhotoImage(Image.open(image_path))
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        if role == "user":
            self.login_screen(role)
        elif role == "admin":
            self.login_screen(role, is_admin=True)



    
    def login_screen(self, role, is_admin=False):
        login_frame = tk.Frame(self.root)
        login_frame.pack(pady=50)

        label_username = tk.Label(login_frame, text="Username:")
        label_password = tk.Label(login_frame, text="Password:")

        entry_username = tk.Entry(login_frame)
        entry_password = tk.Entry(login_frame, show="*")

        label_username.grid(row=0, column=0)
        label_password.grid(row=1, column=0)
        entry_username.grid(row=0, column=1)
        entry_password.grid(row=1, column=1)

        login_button = tk.Button(login_frame, text="Login", command=lambda: self.authenticate(entry_username.get(), entry_password.get(), role, is_admin))
        register_button = tk.Button(login_frame, text="Register", command=self.register_screen)
        forgot_password_button = tk.Button(login_frame, text="Forgot Password", command=self.forgot_password_screen)

        login_button.grid(row=2, column=0, columnspan=2, pady=10)
        register_button.grid(row=3, column=0, columnspan=2)
        forgot_password_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Assuming view_movies_screen is the method responsible for displaying movies
        # Move the call to this method inside the successful login block
        if self.logged_in_user is not None:  # Use your own condition for successful login
            self.view_movies_screen()  # Call the method to display movies

    # Add your other methods (authenticate, register_screen, forgot_password_screen, etc.)



    def register_screen(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Register")

        label_username = tk.Label(register_window, text="Username:")
        label_password = tk.Label(register_window, text="Password:")

        entry_username = tk.Entry(register_window)
        entry_password = tk.Entry(register_window, show="*")

        label_username.grid(row=0, column=0)
        label_password.grid(row=1, column=0)
        entry_username.grid(row=0, column=1)
        entry_password.grid(row=1, column=1)

        register_button = tk.Button(register_window, text="Register", command=lambda: self.register_user(entry_username.get(), entry_password.get()))
        register_button.grid(row=2, column=0, columnspan=2, pady=10)

    def authenticate(self, username, password, role, is_admin=False):
        print(f"Attempting to authenticate user: {username}, role: {role}, is_admin: {is_admin}")
        
        if username in self.users and self.users[username]["password"] == password:
            print("Username and password are valid.")
            if role == "user":
                self.current_user = username
                self.movies = self.load_movies()
                self.main_menu()
            elif role == "admin" and (is_admin or ("role" in self.users[username] and self.users[username]["role"] == "admin")):
                self.current_user = username
                self.movies = self.load_movies()
                self.admin_menu()
            else:
                print("Invalid role or access.")
                messagebox.showerror("Error", "Invalid role or access.")
        else:
            print("Invalid username or password")
            messagebox.showerror("Error", "Invalid username or password")





    def admin_menu(self):
        admin_frame = tk.Frame(self.root)
        admin_frame.pack(pady=20)

        add_movie_button = tk.Button(admin_frame, text="Add Movie", command=self.add_movie_screen)
        view_movies_button = tk.Button(admin_frame, text="View Movies", command=self.view_movies_screen)
        view_ratings_button = tk.Button(admin_frame, text="View Ratings", command=self.view_ratings_screen)
        search_filter_button = tk.Button(admin_frame, text="Search and Filter", command=self.search_and_filter_screen)
        delete_movie_button = tk.Button(admin_frame, text="Delete Movie", command=self.delete_movie_screen)
        edit_movie_button = tk.Button(admin_frame, text="Edit Movie", command=self.edit_movie_screen)
        logout_button = tk.Button(admin_frame, text="Logout", command=self.logout)

        add_movie_button.grid(row=0, column=0, pady=10)
        view_movies_button.grid(row=1, column=0, pady=10)
        view_ratings_button.grid(row=2, column=0, pady=10)
        search_filter_button.grid(row=3, column=0, pady=10)
        delete_movie_button.grid(row=4, column=0, pady=10)
        edit_movie_button.grid(row=5, column=0, pady=10)
        logout_button.grid(row=6, column=0, pady=10)


    def user_menu(self):
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=20)

        add_movie_button = tk.Button(menu_frame, text="Add Movie", command=self.add_movie_screen)
        view_movies_button = tk.Button(menu_frame, text="View Movies", command=self.view_movies_screen)
        view_ratings_button = tk.Button(menu_frame, text="View Ratings", command=self.view_ratings_screen)
        search_filter_button = tk.Button(menu_frame, text="Search and Filter", command=self.search_and_filter_screen)
        logout_button = tk.Button(menu_frame, text="Logout", command=self.logout)

        add_movie_button.grid(row=0, column=0, pady=10)
        view_movies_button.grid(row=1, column=0, pady=10)
        view_ratings_button.grid(row=2, column=0, pady=10)
        search_filter_button.grid(row=3, column=0, pady=10)  # Added Search and Filter button
        logout_button.grid(row=4, column=0, pady=10)


    def register_user(self, username, password, role="user"):
        if username not in self.users:
            # Added a "movies" field and "role" field to the user's dictionary during registration
            self.users[username] = {"password": password, "movies": [], "role": role}
            self.save_data()
            messagebox.showinfo("Success", "Registration successful!")
        else:
            messagebox.showerror("Error", "Username already exists. Choose a different username.")
        # Register a regular user
        self.register_user("new_user", "password")

         # Register an admin user
        self.register_user("admin", "adminpassword", role="admin")


    def search_and_filter_screen(self):
        search_filter_window = tk.Toplevel(self.root)
        search_filter_window.title("Search and Filter")

        label_title = tk.Label(search_filter_window, text="Title:")
        label_genre = tk.Label(search_filter_window, text="Genre:")
        label_director = tk.Label(search_filter_window, text="Director:")
        label_date = tk.Label(search_filter_window, text="Date:")

        entry_title = tk.Entry(search_filter_window)
        entry_genre = tk.Entry(search_filter_window)
        entry_director = tk.Entry(search_filter_window)
        entry_date = tk.Entry(search_filter_window)

        label_title.grid(row=0, column=0)
        label_genre.grid(row=1, column=0)
        label_director.grid(row=2, column=0)
        label_date.grid(row=3, column=0)

        entry_title.grid(row=0, column=1)
        entry_genre.grid(row=1, column=1)
        entry_director.grid(row=2, column=1)
        entry_date.grid(row=3, column=1)

        search_button = tk.Button(search_filter_window, text="Search", command=lambda: self.search_movies(entry_title.get(), entry_genre.get(), entry_director.get(), entry_date.get()))
        search_button.grid(row=4, column=0, columnspan=2, pady=10)

    def search_movies(self, title, genre, director, date):
    # Filter movies based on user input
        filtered_movies = []
        for movie in self.movies:
            title_match = title.lower() in movie["Title"].lower()
            genre_match = genre.lower() in movie["Genre"].lower()
            director_match = director.lower() in movie["Director"].lower()
            date_match = date == "" or date == movie.get("Year", "")  # Check the "Year" field for date match

            # Check if all search criteria match
            if title_match and genre_match and director_match and date_match:
                filtered_movies.append(movie)

        # Sort movies alphabetically by title
        filtered_movies = sorted(filtered_movies, key=lambda x: x["Title"].lower())

        # Display filtered and sorted results
        self.display_search_results(filtered_movies)

    def display_search_results(self, movies):
        search_results_window = tk.Toplevel(self.root)
        search_results_window.title("Search Results")

        text = tk.Text(search_results_window, height=10, width=50)
        text.pack(pady=20)

        for i, movie in enumerate(movies):
            text.insert(tk.END, f"{i + 1}. Title: {movie['Title']}\nYear: {movie['Year']}\nGenre: {movie['Genre']}\nDirector: {movie['Director']}\nCast: {movie['Cast']}\n")
            text.insert(tk.END, f"Rating: {self.get_movie_rating(i)}\n")
            text.insert(tk.END, f"Review: {self.get_movie_review(i)}\n\n")

    def main_menu(self):
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=20)

        add_movie_button = tk.Button(menu_frame, text="Add Movie", command=self.add_movie_screen)
        view_movies_button = tk.Button(menu_frame, text="View Movies", command=self.view_movies_screen)
        view_ratings_button = tk.Button(menu_frame, text="View Ratings", command=self.view_ratings_screen)
        search_filter_button = tk.Button(menu_frame, text="Search and Filter", command=self.search_and_filter_screen)
        logout_button = tk.Button(menu_frame, text="Logout", command=self.logout)

        add_movie_button.grid(row=0, column=0, pady=10)
        view_movies_button.grid(row=1, column=0, pady=10)
        view_ratings_button.grid(row=2, column=0, pady=10)
        search_filter_button.grid(row=3, column=0, pady=10)  # Added Search and Filter button
        logout_button.grid(row=4, column=0, pady=10)

    def add_movie_screen(self):
        add_movie_window = tk.Toplevel(self.root)
        add_movie_window.title("Add Movie")

        label_title = tk.Label(add_movie_window, text="Title:")
        label_year = tk.Label(add_movie_window, text="Year:")
        label_genre = tk.Label(add_movie_window, text="Genre:")
        label_director = tk.Label(add_movie_window, text="Director:")
        label_cast = tk.Label(add_movie_window, text="Cast:")
        label_rating = tk.Label(add_movie_window, text="Rating (1-5):")
        label_review = tk.Label(add_movie_window, text="Review:")

        entry_title = tk.Entry(add_movie_window)
        entry_year = tk.Entry(add_movie_window)
        entry_genre = tk.Entry(add_movie_window)
        entry_director = tk.Entry(add_movie_window)
        entry_cast = tk.Entry(add_movie_window)
        entry_rating = tk.Entry(add_movie_window)
        entry_review = tk.Entry(add_movie_window)

        label_title.grid(row=0, column=0)
        label_year.grid(row=1, column=0)
        label_genre.grid(row=2, column=0)
        label_director.grid(row=3, column=0)
        label_cast.grid(row=4, column=0)
        label_rating.grid(row=5, column=0)
        label_review.grid(row=6, column=0)

        entry_title.grid(row=0, column=1)
        entry_year.grid(row=1, column=1)
        entry_genre.grid(row=2, column=1)
        entry_director.grid(row=3, column=1)
        entry_cast.grid(row=4, column=1)
        entry_rating.grid(row=5, column=1)
        entry_review.grid(row=6, column=1)

        add_button = tk.Button(add_movie_window, text="Add", command=lambda: self.add_movie(
            entry_title.get(), entry_year.get(), entry_genre.get(),
            entry_director.get(), entry_cast.get(), entry_rating.get(), entry_review.get()
        ))
        add_button.grid(row=7, column=0, columnspan=2, pady=10)

    def add_movie(self, title, year, genre, director, cast, rating, review):
        try:
            rating = int(rating)
            if 1 <= rating <= 5:
                self.ratings[len(self.movies)] = rating
            else:
                raise ValueError("Rating must be between 1 and 5.")
        except ValueError:
            messagebox.showerror("Error", "Invalid rating. Please enter a number between 1 and 5.")
            return

        self.reviews[len(self.movies)] = review

        movie = {"Title": title, "Year": year, "Genre": genre, "Director": director, "Cast": cast}
        self.movies.append(movie)
        self.save_data()
        messagebox.showinfo("Success", "Movie added successfully!")

    def view_ratings_screen(self):
        view_ratings_window = tk.Toplevel(self.root)
        view_ratings_window.title("View Ratings")

        text = tk.Text(view_ratings_window, height=10, width=50)
        text.pack(pady=20)

        for i, movie in enumerate(self.movies):
            text.insert(tk.END, f"{i + 1}. Title: {movie['Title']}\n")
            text.insert(tk.END, f"Rating: {self.get_movie_rating(i)}\n\n")


    def view_reviews_screen(self):
        view_reviews_window = tk.Toplevel(self.root)
        view_reviews_window.title("View Reviews")

        text = tk.Text(view_reviews_window, height=10, width=50)
        text.pack(pady=20)

        for i, movie in enumerate(self.movies):
            text.insert(tk.END, f"{i + 1}. Title: {movie['Title']}\n")
            text.insert(tk.END, f"Review: {self.get_movie_review(i)}\n\n")


    def get_movie_rating(self, movie_index):
        return self.ratings.get(movie_index, "Not rated")

    def get_movie_review(self, movie_index):
        return self.reviews.get(movie_index, "No review")

    def rate_movie_screen(self, movie_index):
        rate_movie_window = tk.Toplevel(self.root)
        rate_movie_window.title("Rate Movie")

        label_rating = tk.Label(rate_movie_window, text="Rating (1-5):")
        entry_rating = tk.Entry(rate_movie_window)

        label_rating.grid(row=0, column=0)
        entry_rating.grid(row=0, column=1)

        rate_button = tk.Button(rate_movie_window, text="Rate", command=lambda: self.rate_movie(movie_index, entry_rating.get()))
        rate_button.grid(row=1, column=0, columnspan=2, pady=10)

    def review_movie_screen(self, movie_index):
        review_movie_window = tk.Toplevel(self.root)
        review_movie_window.title("Review Movie")

        label_review = tk.Label(review_movie_window, text="Review:")
        entry_review = tk.Entry(review_movie_window)

        label_review.grid(row=0, column=0)
        entry_review.grid(row=0, column=1)

        review_button = tk.Button(review_movie_window, text="Review", command=lambda: self.review_movie(movie_index, entry_review.get()))
        review_button.grid(row=1, column=0, columnspan=2, pady=10)

    def rate_movie(self, movie_index, rating):
        try:
            rating = int(rating)
            if 1 <= rating <= 5:
                self.ratings[movie_index] = rating
                self.save_data()
                messagebox.showinfo("Success", "Rating submitted successfully!")
            else:
                messagebox.showerror("Error", "Rating must be between 1 and 5.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a number.")

    def review_movie(self, movie_index, review):
        self.reviews[movie_index] = review
        self.save_data()
        messagebox.showinfo("Success", "Review submitted successfully!")


    def get_movie_rating(self, movie_index):
        return self.ratings.get(movie_index, "Not rated")

    def get_movie_review(self, movie_index):
        return self.reviews.get(movie_index, "No review")

    

    def save_data(self):
        # Save users to file
        with open(USER_FILE, "w") as file:
            json.dump(self.users, file, indent=2)

        # Save movies specific to the current user
        if self.current_user in self.users:
            self.users[self.current_user]["movies"] = self.movies
            with open(MOVIE_FILE, "w") as movie_file:
                json.dump(self.movies, movie_file, indent=2)

    def logout(self):
        self.current_user = None
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieManagementSystem(root)
    root.mainloop()
