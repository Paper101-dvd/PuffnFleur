const { createApp } = Vue;

const api = async (url, options = {}) => {
  const res = await fetch(url, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(data.error || "Something went wrong.");
    err.status = res.status;
    throw err;
  }
  return data;
};

const emptyForm = () => ({
  id: null,
  full_name: "",
  email: "",
  phone: "",
  event_type: "",
  preferred_package: "",
  custom_package_details: "",
  event_date: "",
  event_location: "",
  additional_notes: "",
  status: "new",
});

const emptyPackageForm = () => ({
  id: "",
  name: "",
  price: "",
  delivery: true,
  image: "",
  featuresText: "", // one feature per line in the textarea
});

createApp({
  data() {
    return {
      loading: true,
      view: "login", // login | register | dashboard
      user: null,
      error: "",

      loginForm: { username: "", password: "" },
      registerForm: { username: "", email: "", password: "" },

      tab: "bookings", // bookings | packages

      bookings: [],
      total: 0,
      eventCounts: {},
      search: "",
      eventFilter: "",
      packageFilter: "",

      showModal: false,
      modalMode: "create", // create | edit
      form: emptyForm(),
      formError: "",

      packages: [],
      showPackageModal: false,
      packageModalMode: "create", // create | edit
      packageForm: emptyPackageForm(),
      packageFormError: "",
    };
  },

  computed: {
    eventTypeOptions() {
      return Object.keys(this.eventCounts);
    },
  },

  async mounted() {
    try {
      const { user } = await api("/api/auth/me");
      if (user) {
        this.user = user;
        this.view = "dashboard";
        await Promise.all([this.loadBookings(), this.loadPackages()]);
      }
    } finally {
      this.loading = false;
    }
  },

  methods: {
    // ---------- auth ----------
    async login() {
      this.error = "";
      try {
        const { user } = await api("/api/auth/login", {
          method: "POST",
          body: JSON.stringify(this.loginForm),
        });
        this.user = user;
        this.view = "dashboard";
        await Promise.all([this.loadBookings(), this.loadPackages()]);
      } catch (e) {
        this.error = e.message;
      }
    },

    async register() {
      this.error = "";
      try {
        const { user } = await api("/api/auth/register", {
          method: "POST",
          body: JSON.stringify(this.registerForm),
        });
        this.user = user;
        this.view = "dashboard";
        await Promise.all([this.loadBookings(), this.loadPackages()]);
      } catch (e) {
        this.error = e.message;
      }
    },

    async logout() {
      await api("/api/auth/logout", { method: "POST" });
      this.user = null;
      this.view = "login";
      this.bookings = [];
    },

    switchView(v) {
      this.error = "";
      this.view = v;
    },

    // ---------- bookings (CRUD) ----------
    async loadBookings() {
      const params = new URLSearchParams();
      if (this.search) params.set("search", this.search);
      if (this.eventFilter) params.set("event_type", this.eventFilter);
      if (this.packageFilter) params.set("package", this.packageFilter);

      const data = await api(`/api/bookings?${params.toString()}`);
      this.bookings = data.bookings;
      this.total = data.total;
      this.eventCounts = data.event_counts;
    },

    openCreate() {
      this.modalMode = "create";
      this.form = emptyForm();
      this.formError = "";
      this.showModal = true;
    },

    openEdit(booking) {
      this.modalMode = "edit";
      this.form = { ...emptyForm(), ...booking };
      this.formError = "";
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
    },

    async saveBooking() {
      this.formError = "";
      try {
        if (this.modalMode === "create") {
          await api("/api/bookings", { method: "POST", body: JSON.stringify(this.form) });
        } else {
          await api(`/api/bookings/${this.form.id}`, { method: "PUT", body: JSON.stringify(this.form) });
        }
        this.showModal = false;
        await this.loadBookings();
      } catch (e) {
        this.formError = e.message;
      }
    },

    async deleteBooking(booking) {
      if (!confirm(`Delete the booking for ${booking.full_name}? This can't be undone.`)) return;
      await api(`/api/bookings/${booking.id}`, { method: "DELETE" });
      await this.loadBookings();
    },

    switchTab(t) {
      this.tab = t;
    },

    // ---------- packages (CRUD: prices, features, custom packages) ----------
    async loadPackages() {
      const data = await api("/api/packages");
      this.packages = data.packages;
    },

    openCreatePackage() {
      this.packageModalMode = "create";
      this.packageForm = emptyPackageForm();
      this.packageFormError = "";
      this.showPackageModal = true;
    },

    openEditPackage(pkg) {
      this.packageModalMode = "edit";
      this.packageForm = {
        id: pkg.id,
        name: pkg.name,
        price: pkg.price,
        delivery: pkg.delivery,
        image: pkg.image || "",
        featuresText: (pkg.features || []).join("\n"),
      };
      this.packageFormError = "";
      this.showPackageModal = true;
    },

    closePackageModal() {
      this.showPackageModal = false;
    },

    async savePackage() {
      this.packageFormError = "";
      const payload = {
        name: this.packageForm.name,
        price: this.packageForm.price,
        delivery: this.packageForm.delivery,
        image: this.packageForm.image,
        features: this.packageForm.featuresText,
      };
      try {
        if (this.packageModalMode === "create") {
          payload.id = this.packageForm.id;
          await api("/api/packages", { method: "POST", body: JSON.stringify(payload) });
        } else {
          await api(`/api/packages/${this.packageForm.id}`, { method: "PUT", body: JSON.stringify(payload) });
        }
        this.showPackageModal = false;
        await this.loadPackages();
      } catch (e) {
        this.packageFormError = e.message;
      }
    },

    async deletePackage(pkg) {
      if (!confirm(`Delete "${pkg.name}"? This can't be undone.`)) return;
      await api(`/api/packages/${pkg.id}`, { method: "DELETE" });
      await this.loadPackages();
    },
  },

  template: `
    <div v-if="loading" class="auth-wrap"><p>Loading…</p></div>

    <div v-else-if="view === 'login'" class="auth-wrap">
      <div class="auth-card">
        <div class="auth-logo">
          <div class="badge">PF</div>
          <h1>Puff n' Fleur</h1>
          <p>Admin Sign In</p>
        </div>
        <div v-if="error" class="alert-box">{{ error }}</div>
        <form @submit.prevent="login">
          <div class="field">
            <label>Username</label>
            <input v-model="loginForm.username" required autofocus placeholder="admin" />
          </div>
          <div class="field">
            <label>Password</label>
            <input type="password" v-model="loginForm.password" required placeholder="••••••••" />
          </div>
          <button type="submit" class="btn btn-primary">Sign In</button>
        </form>
        <p class="switch-link">No account yet? <a @click="switchView('register')">Register</a></p>
        <p class="switch-link"><a href="/">&larr; Back to site</a></p>
      </div>
    </div>

    <div v-else-if="view === 'register'" class="auth-wrap">
      <div class="auth-card">
        <div class="auth-logo">
          <div class="badge">PF</div>
          <h1>Create Admin Account</h1>
          <p>Puff n' Fleur</p>
        </div>
        <div v-if="error" class="alert-box">{{ error }}</div>
        <form @submit.prevent="register">
          <div class="field">
            <label>Username</label>
            <input v-model="registerForm.username" required autofocus />
          </div>
          <div class="field">
            <label>Email</label>
            <input type="email" v-model="registerForm.email" required />
          </div>
          <div class="field">
            <label>Password</label>
            <input type="password" v-model="registerForm.password" required minlength="6" placeholder="At least 6 characters" />
          </div>
          <button type="submit" class="btn btn-primary">Create Account</button>
        </form>
        <p class="switch-link">Already have an account? <a @click="switchView('login')">Sign in</a></p>
      </div>
    </div>

    <div v-else>
      <header class="dash-header">
        <h1>Puff n' Fleur — Bookings</h1>
        <div class="user-info">
          <span>Signed in as <strong>{{ user.username }}</strong></span>
          <a class="back-link" href="/">View site</a>
          <button class="btn btn-secondary btn-small" @click="logout">Log out</button>
        </div>
      </header>

      <nav class="tab-nav">
        <button :class="['tab-btn', { active: tab === 'bookings' }]" @click="switchTab('bookings')">Bookings</button>
        <button :class="['tab-btn', { active: tab === 'packages' }]" @click="switchTab('packages')">Packages &amp; Pricing</button>
      </nav>

      <div class="dash-body" v-if="tab === 'bookings'">
        <div class="stats-row">
          <div class="stat-card"><div class="num">{{ total }}</div><div class="label">Total Bookings</div></div>
          <div class="stat-card" v-for="(count, type) in eventCounts" :key="type">
            <div class="num">{{ count }}</div><div class="label">{{ type }}</div>
          </div>
        </div>

        <div class="toolbar">
          <div class="filters">
            <input placeholder="Search name, email, location…" v-model="search" @input="loadBookings" />
            <select v-model="eventFilter" @change="loadBookings">
              <option value="">All event types</option>
              <option v-for="t in eventTypeOptions" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>
          <button class="btn btn-primary btn-small" @click="openCreate">+ New Booking</button>
        </div>

        <div class="table-wrap">
          <table v-if="bookings.length">
            <thead>
              <tr>
                <th>Name</th><th>Email</th><th>Phone</th><th>Event</th>
                <th>Package</th><th>Date</th><th>Location</th><th>Status</th><th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="b in bookings" :key="b.id">
                <td>{{ b.full_name }}</td>
                <td>{{ b.email }}</td>
                <td>{{ b.phone }}</td>
                <td>{{ b.event_type }}</td>
                <td>
                  {{ b.preferred_package || '—' }}
                  <div v-if="b.preferred_package === 'Custom' && b.custom_package_details" class="custom-note" :title="b.custom_package_details">📝</div>
                </td>
                <td>{{ b.event_date }}</td>
                <td>{{ b.event_location }}</td>
                <td><span :class="'status-pill status-' + b.status">{{ b.status }}</span></td>
                <td class="row-actions">
                  <button class="btn btn-secondary btn-small" @click="openEdit(b)">Edit</button>
                  <button class="btn btn-danger btn-small" @click="deleteBooking(b)">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else class="empty-state">No bookings match your filters yet.</div>
        </div>
      </div>

      <div class="dash-body" v-if="tab === 'packages'">
        <div class="toolbar">
          <p class="muted">Prices and features shown on the public site come from here.</p>
          <button class="btn btn-primary btn-small" @click="openCreatePackage">+ New Package</button>
        </div>

        <div class="table-wrap">
          <table v-if="packages.length">
            <thead>
              <tr>
                <th>ID</th><th>Name</th><th>Price</th><th>Delivery</th><th>Features</th><th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in packages" :key="p.id">
                <td>{{ p.id }}</td>
                <td>{{ p.name }}</td>
                <td>\${{ p.price }}</td>
                <td>{{ p.delivery ? 'Included' : 'Not included' }}</td>
                <td>{{ p.features.length }} listed</td>
                <td class="row-actions">
                  <button class="btn btn-secondary btn-small" @click="openEditPackage(p)">Edit</button>
                  <button class="btn btn-danger btn-small" @click="deletePackage(p)">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else class="empty-state">No packages yet.</div>
        </div>
      </div>

      <div v-if="showModal" class="modal-backdrop" @click.self="closeModal">
        <div class="modal-card">
          <h2>{{ modalMode === 'create' ? 'New Booking' : 'Edit Booking' }}</h2>
          <div v-if="formError" class="alert-box">{{ formError }}</div>
          <form @submit.prevent="saveBooking">
            <div class="two-col">
              <div class="field"><label>Full Name</label><input v-model="form.full_name" required /></div>
              <div class="field"><label>Email</label><input type="email" v-model="form.email" required /></div>
            </div>
            <div class="two-col">
              <div class="field"><label>Phone</label><input v-model="form.phone" required /></div>
              <div class="field"><label>Event Date</label><input type="date" v-model="form.event_date" required /></div>
            </div>
            <div class="two-col">
              <div class="field">
                <label>Event Type</label>
                <select v-model="form.event_type" required>
                  <option value="">Select an event type</option>
                  <option value="Birthday">Birthday Party</option>
                  <option value="Baby Shower">Baby Shower</option>
                  <option value="Wedding">Wedding</option>
                  <option value="Graduation">Graduation Party</option>
                  <option value="Corporate">Corporate Event</option>
                  <option value="Family Gathering">Family Gathering</option>
                  <option value="Holiday Party">Holiday Party</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              <div class="field">
                <label>Preferred Package</label>
                <select v-model="form.preferred_package">
                  <option value="">None</option>
                  <option v-for="p in packages" :key="p.id" :value="p.name">{{ p.name }} (\${{ p.price }})</option>
                  <option value="Custom">Custom</option>
                </select>
              </div>
            </div>
            <div class="field" v-if="form.preferred_package === 'Custom'">
              <label>Custom Package Details</label>
              <textarea v-model="form.custom_package_details" rows="3" placeholder="What should this custom package include?"></textarea>
            </div>
            <div class="field"><label>Event Location</label><input v-model="form.event_location" required /></div>
            <div class="field"><label>Notes</label><textarea v-model="form.additional_notes" rows="3"></textarea></div>
            <div class="field" v-if="modalMode === 'edit'">
              <label>Status</label>
              <select v-model="form.status">
                <option value="new">New</option>
                <option value="contacted">Contacted</option>
                <option value="confirmed">Confirmed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
            <div class="modal-actions">
              <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
              <button type="submit" class="btn btn-primary">{{ modalMode === 'create' ? 'Create' : 'Save Changes' }}</button>
            </div>
          </form>
        </div>
      </div>

      <div v-if="showPackageModal" class="modal-backdrop" @click.self="closePackageModal">
        <div class="modal-card">
          <h2>{{ packageModalMode === 'create' ? 'New Package' : 'Edit Package' }}</h2>
          <div v-if="packageFormError" class="alert-box">{{ packageFormError }}</div>
          <form @submit.prevent="savePackage">
            <div class="two-col">
              <div class="field">
                <label>ID</label>
                <input v-model="packageForm.id" required :disabled="packageModalMode === 'edit'" placeholder="e.g. D or custom-gold" />
              </div>
              <div class="field"><label>Name</label><input v-model="packageForm.name" required /></div>
            </div>
            <div class="two-col">
              <div class="field"><label>Price ($)</label><input type="number" step="0.01" min="0" v-model="packageForm.price" required /></div>
              <div class="field checkbox-field">
                <label><input type="checkbox" v-model="packageForm.delivery" /> Delivery included</label>
              </div>
            </div>
            <div class="field"><label>Image filename</label><input v-model="packageForm.image" placeholder="package-d.jpg" /></div>
            <div class="field">
              <label>Features (one per line)</label>
              <textarea v-model="packageForm.featuresText" rows="4" placeholder="One Backdrop&#10;Balloon garland with up to 3 colors"></textarea>
            </div>
            <div class="modal-actions">
              <button type="button" class="btn btn-secondary" @click="closePackageModal">Cancel</button>
              <button type="submit" class="btn btn-primary">{{ packageModalMode === 'create' ? 'Create' : 'Save Changes' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  `,
}).mount("#app");
