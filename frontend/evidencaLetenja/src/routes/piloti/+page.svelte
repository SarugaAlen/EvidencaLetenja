<script lang="ts">
  import * as Table from "$lib/components/ui/table/index.js";
  import { Button } from "$lib/components/ui/button";
  import { onMount } from "svelte";
  import EditPilotDialog from "$lib/components/ui/editPilot/editPilotDialog.svelte";
  import AddPilotDialog from "$lib/components/ui/addPilot/addPilotDialog.svelte";

  interface Pilot {
    idPilot: number;
    ime: string;
    priimek: string;
  }
  let piloti: Pilot[] = [];

  async function fetchPilots() {
    const response = await fetch(`http://localhost:8000/pridobiPilote/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      console.error("Failed to fetch pilots:", response.statusText);
      return;
    }

    const data = await response.json();
    piloti = data;
  }

  async function handlePilotSave(pilotData: { ime: string; priimek: string }) {
    try {
      const response = await fetch("http://localhost:8000/dodajPilota/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(pilotData),
      });

      if (!response.ok) {
        throw new Error("Failed to save pilot data");
      }

      const result = await response.json();
      console.log("Pilot saved successfully:", result);
      refreshPage();
    } catch (error) {
      console.error("Error saving pilot:", error);
    }
  }

  async function handleEditSave(updatedPilotData: Pilot) {
    try {
      const response = await fetch(
        `http://localhost:8000/pilot/${updatedPilotData.idPilot}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(updatedPilotData),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to update pilot data");
      }

      console.log("Pilot updated successfully:", updatedPilotData);
      refreshPage();
    } catch (error) {
      console.error("Error updating pilot:", error);
    }
  }

  async function deletePilot(id: number) {
    const response = await fetch(`http://localhost:8000/pilot/${id}`, {
      method: "DELETE",
    });
    if (response.ok) {
      piloti = piloti.filter((pilot) => pilot.idPilot !== id);
      console.log("Pilot deleted:", id);
    }
  }

  function refreshPage() {
    fetchPilots();
  }

  onMount(() => {
    fetchPilots();
  });
</script>

<main class="max-w-7xl mx-auto px-4 py-8">
  <section>
    <h1
      class="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl mb-6"
    >
      Piloti
    </h1>
  </section>
  <section>
    <AddPilotDialog
      pilot={{idPilot: 0 , ime: "", priimek: "" }}
      onSave={handlePilotSave}
    />
  </section>
  <section>
    <Table.Root>
      <Table.Header>
        <Table.Row class="table-row">
          <Table.Head class="w-[100px]">ID</Table.Head>
          <Table.Head class="text-right">Ime</Table.Head>
          <Table.Head class="text-right">Priimek</Table.Head>
        </Table.Row>
      </Table.Header>
      <Table.Body>
        {#each piloti as pilot}
          <Table.Row>
            <Table.Cell>{pilot.idPilot}</Table.Cell>
            <Table.Cell class="text-right">{pilot.ime}</Table.Cell>
            <Table.Cell class="text-right">{pilot.priimek}</Table.Cell>
            <Table.Cell class="text-right">
              <EditPilotDialog {pilot} onSave={handleEditSave}
              ></EditPilotDialog>
              <Button
                class="bg-red-500 text-white"
                on:click={() => deletePilot(pilot.idPilot)}>Delete</Button
              >
            </Table.Cell>
          </Table.Row>
        {/each}
      </Table.Body>
    </Table.Root>
  </section>
</main>
