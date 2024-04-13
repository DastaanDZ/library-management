<template>
  <div class="parent-div">
    <div class="main-page">
      <h1>LIBRARIAN</h1>
      <UserDetail :username="username" :userId="userId" />
      <LibrarianAction />
      <BooksAvailable :books="books" :heading="booksAvailable" />
      <BooksAvailable :books="issuedBooks" :heading="booksToBeAssigned" />
    </div>
  </div>
</template>

<script>
import BooksAvailable from "@/components/BooksAvailable.vue";
import NewArrival from "@/components/NewArrival.vue";
import UserDetail from "@/components/UserDetail.vue";
import LibrarianAction from "@/components/LibrarianAction.vue";

import axios from "axios";
import { jwtDecode } from "jwt-decode";

export default {
  name: "Librarian",
  props: ["roleRequired"],
  components: {
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
      userId: "",
      username: "",
      books: [],
      assignedBooks: [],
      issuedBooks: [],
      booksAvailable: "Books Available",
      booksToBeAssigned: "Books To be Assigned",
    };
  },
  mounted() {
    const userRole = localStorage.getItem("role");

    if (userRole !== this.roleRequired) {
      this.$router.push("/login");
      return;
    }
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
      this.userId = user_id;

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
        if (error.response && error.response.status === 401) {
          window.location.href = "/login";
        } else {
          console.error("Error fetching user info:", error);
        }
      }

      try {
        const booksResponse = await axios.get(`http://127.0.0.1:5000/books`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.books = booksResponse.data;
        console.log(this.books);
      } catch (error) {
        if (error.response && error.response.status === 401) {
          window.location.href = "/login";
        } else {
          console.error("Error fetching books:", error);
        }
      }

      try {
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
        if (error.response && error.response.status === 401) {
          window.location.href = "/login";
        } else {
          console.error("Error fetching issued books:", error);
        }
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
