<script lang="ts">
import * as Table from "$lib/components/ui/table/index.js";
import { Button } from "$lib/components/ui/button";
import AddFlightDialog from "./addFlightDialog.svelte";
import { onMount } from "svelte";
import { DateFormatter, type DateValue, getLocalTimeZone } from "@internationalized/date";


  interface Polet {
    idPolet: number;
    cas_vzleta: string;
    cas_pristanka: string;
    Pilot_idPilot: number;
  }

  let poleti: Polet[] = [];
  
  async function fetchFlightsBeforeDate(date: string) {
        const response = await fetch(`http://localhost:8000/pridobiPolet/`);
        if (!response.ok) {
            console.error("Failed to fetch flights:", response.statusText);
            return;
        }
        const data = await response.json();
        poleti = data;
  }  

async function deleteFlight(id: number) {
        const response = await fetch(`http://localhost:8000/polet/${id}`, {
            method: "DELETE",
        });
        if (response.ok) {
            poleti = poleti.filter((polet) => polet.idPolet !== id);
            console.log("Flight deleted:", id);
        } else {
            console.error("Failed to delete flight:", response.statusText);
        }
    }

  async function handleFlightSave(flightData: { cas_vzleta: string; cas_pristanka: string; id_pilota: number }) {
        console.log("Flight data received in parent component:", flightData);
        try {
            const response = await fetch('http://localhost:8000/dodajPolet/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(flightData),
            });

            if (!response.ok) {
                throw new Error('Failed to save flight data');
            }

            const result = await response.json();
            console.log("Flight saved successfully:", result);

        } catch (error) {
            console.error("Error saving flight:", error);
        }
    }


    onMount(() => {
        const today = new Date().toISOString().split("T")[0];
        fetchFlightsBeforeDate(today);
    });
</script>

<main class="max-w-7xl mx-auto px-4 py-8">
    <section>
        <h1
            class="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl mb-6"
        >
            Moji leti
        </h1>
    </section>
    <section>
        <AddFlightDialog onSave={handleFlightSave} />
    </section>
    <section>
        <Table.Root>
            <Table.Header>
                <Table.Row class="table-row">
                    <Table.Head class="w-[100px]">ID</Table.Head>
                    <Table.Head class="text-right">Čas vzleta</Table.Head>
                    <Table.Head class="text-right">Čas pristanka</Table.Head>
                    <Table.Head class="text-right">Pilot ID</Table.Head>
                </Table.Row>
            </Table.Header>
            <Table.Body>
                {#each poleti as polet}
                    <Table.Row>
                        <Table.Cell>{polet.idPolet}</Table.Cell>
                        <Table.Cell
                            >{new Date(polet.cas_vzleta).toLocaleString("sl-SI", { dateStyle: "short", timeStyle: "short" })}</Table.Cell
                        >
                        <Table.Cell class="text-right"
                            >{new Date(polet.cas_pristanka).toLocaleString("sl-SI", { dateStyle: "short", timeStyle: "short" })}</Table.Cell
                        >
                        <Table.Cell class="text-right"
                            >{polet.Pilot_idPilot}</Table.Cell
                        >
                        <Table.Cell class="text-right">
                            <Button on:click={() => editFlight(polet.idPolet)}
                                >Edit</Button
                            >
                            <Button on:click={() => deleteFlight(polet.idPolet)}
                                >Delete</Button
                            >
                        </Table.Cell>
                    </Table.Row>
                {/each}
            </Table.Body>
        </Table.Root>
    </section>
</main>
