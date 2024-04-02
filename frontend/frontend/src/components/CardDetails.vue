<template>
  <div
    class="h-100 d-flex justify-content-center align-items-center min-vh-100"
  >
    <div v-if="book" class="card mb-3" style="max-width: 900px">
      <div class="row g-0">
        <div class="col-md-4">
          <img
            src="./book.jpg"
            class="img-fluid rounded-start"
            alt="Book Cover"
          />
        </div>
        <div class="col-md-8">
          <div class="card-body">
            <h5 class="card-title">{{ book.name }}</h5>
            <p class="card-text">{{ book.description }}</p>
            <p class="card-text">
              <small class="text-muted"
                >Last updated: {{ book.lastUpdated }}</small
              >
            </p>
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

export default {
  name: "CardDetails",
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      book: null,
    };
  },
  mounted() {
    // Fetch book details based on the ID prop
    this.fetchBookDetails();
  },
  methods: {
    async fetchBookDetails() {
      // Make a GET request to the /books/<id> endpoint using Axios
      const accessToken = localStorage.getItem("accessToken");

      if (!accessToken) {
        console.error("Access token not found in localStorage");
        return;
      }

      try {
        await axios
          .get(`http://127.0.0.1:5000/books/${this.id}`, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          })
          .then((response) => {
            // Handle successful response
            this.book = response.data;
          })
          .catch((error) => {
            // Handle error
            console.error("Error fetching book details:", error);
          });
      } catch (error) {
        console.error("Error fetching user book info:", error);
      }
    },
  },
};
</script>
