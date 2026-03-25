<script>
  import { appState } from "./appState.svelte";
  let { assoc_id, product_id, location_id, expiration_date } = $props();

  let location_name = $derived(
    appState.locations.find((l) => l.id === location_id)?.name || "Unknown",
  );
</script>

<div class="">
  <!-- TODO: Add a delete button. Maybe also a notes section? -->
  <div>Product: {appState.product.name}</div>
  <!-- TODO: Change to Drop-Down menu to move around -->
  <div>Location: {location_name}</div>
  <div>Expires: {expiration_date}</div>
</div>
