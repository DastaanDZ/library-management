<template>
  <div class="assign-section-page">
    <h1>Assign Book to Section</h1>
    <form @submit.prevent="assignBook" class="d-flex mw-100">
      <div class="form-group text-start mb-1">
        <label for="book">Select Book:</label>
        <input
          type="text"
          v-model="selectedBook"
          class="form-control item"
          id="book"
        />
      </div>
      <div class="form-group text-start mb-1 mr-1">
        <button
          type="button"
          class="btn btn-primary create-account"
          @click="filterBooks"
        >
          Filter
        </button>
      </div>
      <div class="form-group text-start mb-1">
        <label for="section">Select Section:</label>
        <select
          v-model="selectedSection"
          class="form-control item"
          id="section"
        >
          <option value="">All Sections</option>
          <option
            v-for="section in sections"
            :key="section.id"
            :value="section.name"
          >
            {{ section.name }}
          </option>
        </select>
      </div>
      <div class="form-group text-start mb-1">
        <button
          type="button"
          class="btn btn-primary create-account"
          @click="filterSections"
        >
          Filter
        </button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "SearchBar",
  props: {
    sections: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      selectedBook: "",
      selectedSection: "",
      filteredSections: [],
    };
  },
  methods: {
    filterSections() {
      console.log("Inside Filter Sections");
      console.log(this.selectedSection);
      this.filteredSections = this.sections.filter(
        (section) => section.name == this.selectedSection
      );
      console.log("AFTER FILTERING");
      console.log(this.filteredSections);
      console.log("Bookd in after filtering");
      console.log(this.filteredSections[0].books);
      this.$emit("filteredData", this.filteredSections[0].books);
    },
    filterBooks() {
      try {
        // Implement the logic to assign the selected book to the selected section
        console.log("Inside search");
        console.log(this.selectedBook);
        console.log("Sections");
        console.log(this.sections);

        const filteredBooks = this.sections.reduce((accumulator, section) => {
          const books = section.books.filter((book) =>
            book.name.toLowerCase().includes(this.selectedBook.toLowerCase())
          );
          return accumulator.concat(books);
        }, []);

        console.log("after filtering search");
        console.log(filteredBooks);
        //   console.log(this.filteredSections);

        this.$emit("filteredData", filteredBooks);
      } catch (error) {
        console.error("Error filtering books:", error);
        if (error.response && error.response.status === 404) {
          // Redirect to login page if unauthorized (status code 404)
          this.$router.push("/login");
        }
      }
    },
  },
};
</script>
