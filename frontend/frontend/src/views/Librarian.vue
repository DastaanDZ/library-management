<template>
  <div class="parent-div">
    <Navbar />
    <div class="main-page">
      <h1>LIBRARIAN</h1>
      <UserDetail :username="username" />
      <LibrarianAction />
      <BooksAvailable :books="books" :heading="booksAvailable" />
      <BooksAvailable :books="issuedBooks" :heading="booksToBeAssigned" />
    </div>
  </div>
</template>

<script>
import BookIssued from "@/components/BookIssued.vue";
import BookRequested from "@/components/BookRequested.vue";
import BookReturned from "@/components/BookReturned.vue";
import BooksAvailable from "@/components/BooksAvailable.vue";
import Navbar from "@/components/Navbar.vue";
import NewArrival from "@/components/NewArrival.vue";
import UserDetail from "@/components/UserDetail.vue";
import LibrarianAction from "@/components/LibrarianAction.vue";

import axios from "axios";
import { jwtDecode } from "jwt-decode";

export default {
  name: "Librarian",
  props: ["roleRequired"],
  components: {
    Navbar,
    UserDetail,
    BookIssued,
    BookRequested,
    BookReturned,
    BooksAvailable,
    NewArrival,
    LibrarianAction,
  },
  data() {
    return {
      username: "", // Initialize username as an empty string
      books: [],
      assignedBooks: [],
      issuedBooks: [],
      booksAvailable: "Books Available",
      booksToBeAssigned: "Books To be Assigned",
    };
  },
  mounted() {
    const userRole = localStorage.getItem("role");

    // Check if user role matches the required role
    if (userRole !== this.roleRequired) {
      // Redirect to login page
      this.$router.push("/login");
      return;
    }

    // Fetch user information if the role matches
    this.fetchUserInfo();
  },
  methods: {
    async fetchUserInfo() {
      const accessToken = localStorage.getItem("accessToken");

      if (!accessToken) {
        console.error("Access token not found in localStorage");
        return;
      }

      const decodedToken = jwtDecode(accessToken);
      const user_id = decodedToken.sub;

      try {
        const userInfoResponse = await axios.get(
          `http://127.0.0.1:5000/user-info/${user_id}`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        this.username = userInfoResponse.data.username;
      } catch (error) {
        console.error("Error fetching user info:", error);
      }

      try {
        // Fetch books
        const booksResponse = await axios.get(`http://127.0.0.1:5000/books`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.books = booksResponse.data; // Assign directly to this.books
        console.log(this.books);
      } catch (error) {
        console.error("Error fetching books:", error);
      }

      try {
        // Fetch unique books requested
        const issuedBooksResponse = await axios.get(
          `http://127.0.0.1:5000/unique-books-requested`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        this.issuedBooks = issuedBooksResponse.data.unique_books;
        console.log(this.issuedBooks);
      } catch (error) {
        console.error("Error fetching issued books:", error);
      }
    },
  },
};
</script>

<style scoped>
.parent-div {
  display: flex;
  flex-direction: column;
  padding: 0 2rem;
  gap: 2rem;
}
.main-page {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
</style>
