<template>
  <div
    class="h-100 d-flex justify-content-center align-items-center min-vh-100"
  >
    <div v-if="book" class="card mb-3" style="max-width: 900px">
      <div class="row g-0">
        <div class="col-md-4">
          <img
            :src="book.link"
            class="img-fluid rounded-start"
            alt="Book Cover"
          />
        </div>
        <div class="col-md-8">
          <div class="card-body text-start">
            <h5>Name</h5>
            <h5 class="card-title">{{ book.name }}</h5>
            <p>Content</p>
            <p class="card-text">{{ book.content }}</p>
            <p>Author</p>
            <p class="card-text">{{ book.author }}</p>
            <p>Price</p>
            <p class="card-text">{{ book.price }}</p>
            <p class="card-text">
              <small class="text-muted"
                >Last updated: {{ book.lastUpdated }}</small
              >
            </p>

            <h3>Books Have to be Assigned</h3>
            <button
              v-for="user in requestedUsers"
              :key="user.userId"
              @click="issueBook(user.userId, book_id)"
              class="btn btn-primary m-2"
            >
              {{ user.username }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { jwtDecode } from "jwt-decode";

export default {
  name: "LibCardDetails",
  props: {
    book_id: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      book: null,
      requestedUsers: [],
    };
  },
  created() {
    this.accessToken = localStorage.getItem("accessToken");
  },
  mounted() {
    this.fetchBookDetails();
    this.fetchRequestedUsers();
  },
  methods: {
    async fetchBookDetails() {
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/books/${this.book_id}`,
          {
            headers: {
              Authorization: `Bearer ${this.accessToken}`,
            },
          }
        );
        this.book = response.data;
      } catch (error) {
        console.error("Error fetching book details", error);
        if (error.response && error.response.status === 401) {
          this.$router.push("/login");
        }
      }
    },

    async fetchRequestedUsers() {
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/users-requested/${this.book_id}`,
          {
            headers: {
              Authorization: `Bearer ${this.accessToken}`,
            },
          }
        );

        this.requestedUsers = response.data.requested_users;
        console.log("USERS requested this book", this.requestedUsers);
        await Promise.all(
          this.requestedUsers.map(async (userId, index) => {
            try {
              const userResponse = await axios.get(
                `http://127.0.0.1:5000/user-info/${userId}`,
                {
                  headers: {
                    Authorization: `Bearer ${this.accessToken}`,
                  },
                }
              );
              console.log("USER RESPONSE", userResponse);
              this.$set(this.requestedUsers, index, {
                userId,
                username: userResponse.data.username,
              });
              console.log("Username and ID", this.requestedUsers);
            } catch (error) {
              console.error("Error fetching user info:", error);
              if (error.response && error.response.status === 401) {
                this.$router.push("/login");
              }
            }
          })
        );
      } catch (error) {
        console.error("Error fetching requested users: ", error);
        if (error.response && error.response.status === 401) {
          this.$router.push("/login");
        }
      }
    },
    async issueBook(userId, bookId) {
      try {
        const issueResponse = await axios.post(
          `http://127.0.0.1:5000/issue-book/${userId}`,
          { book_id: [bookId] },
          {
            headers: {
              Authorization: `Bearer ${this.accessToken}`,
            },
          }
        );

        console.log("BOOK ISSUED", issueResponse);

        const requestIdResponse = await axios.get(
          `http://127.0.0.1:5000/request-id?book_id=${bookId}&user_id=${userId}`,
          {
            headers: {
              Authorization: `Bearer ${this.accessToken}`,
            },
          }
        );
        const requestId = requestIdResponse.data.request_id;

        const removeRequestResponse = await axios.delete(
          `http://127.0.0.1:5000/remove-request/${requestId}`,
          {
            headers: {
              Authorization: `Bearer ${this.accessToken}`,
            },
          }
        );

        console.log("REQUEST REMOVED", removeRequestResponse);
        this.fetchRequestedUsers();
        alert("Assigned book to the user and removed request successfully");
      } catch (error) {
        console.error("Error issuing book: ", error);
        if (error.response && error.response.status === 401) {
          this.$router.push("/login");
        }
      }
    },
  },
};
</script>
