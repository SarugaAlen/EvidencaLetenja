<script lang="ts">
    import * as Table from "$lib/components/ui/table/index.js";
    import { Button } from "$lib/components/ui/button";
    import { onMount } from "svelte";

    interface Polet {
        idPolet: number;
        cas_vzleta: string;
        cas_pristanka: string;
        Pilot_idPilot: number;
    }

    let poleti: Polet[] = [];

    async function fetchFlightsBeforeDate(date: string) {
        const response = await fetch(
            `http://localhost:8000/pridobiPolet/`,
        );
        if (!response.ok) {
            console.error("Failed to fetch flights:", response.statusText);
            return;
        }
        const data = await response.json();
        poleti = data;
    }

    async function editFlight(id: number) {
        console.log("Edit flight with ID:", id);
    }

    async function deleteFlight(id: number) {
        const response = await fetch(`http://localhost:8000/polet/${id}`, { method: "DELETE" });
        if (response.ok) {
            poleti = poleti.filter(polet => polet.idPolet !== id);
            console.log("Flight deleted:", id);
        } else {
            console.error("Failed to delete flight:", response.statusText);
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
        <Table.Root>
            <Table.Caption>Pregled prihajajočih letov</Table.Caption>
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
                            >{new Date(
                                Number(polet.cas_vzleta) * 1000,
                            ).toLocaleDateString("sl-SI")}</Table.Cell
                        >
                        <Table.Cell class="text-right"
                            >{new Date(
                                Number(polet.cas_pristanka) * 1000,
                            ).toLocaleTimeString("sl-SI")}</Table.Cell
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

<style>
</style>
