<script lang="ts">
    import * as Carousel from "$lib/components/ui/carousel/index.js";
    import Button from "@/components/ui/button/button.svelte";
    import { onMount } from "svelte";
    import * as Table from "$lib/components/ui/table/index.js";
    import { Cell } from "@/components/ui/calendar";
    
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

    console.log('API URL:', apiUrl);



    type Pilot = {
      idPilot: number;
      ime: string;
      priimek: string;
    };

    let newPilot: Pilot = { idPilot: 0, ime: "", priimek: "" };
  
    let piloti: Pilot[] = [];
  
    async function getPilots() {
      try {
        const response = await fetch(`${apiUrl}/pridobiPilote/`);
        if (response.ok) {
            piloti = await response.json();
        } else {
          console.error("Failed to fetch pilots data");
        }
      } catch (error) {
        console.error("Error fetching pilots data:", error);
        ///
      }
    }

    async function addPilot() {
        try {
            const response = await fetch(`${apiUrl}/dodajPilota`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(newPilot),
            });
            if (response.ok) {
                const addedPilot = await response.json();
                piloti = [...piloti, addedPilot];
                newPilot = { idPilot: 0, ime: "", priimek: "" }; 
                console.log("Pilot successfully added:", addedPilot);
            } else {
                console.error("Failed to add pilot:", response.statusText);
            }
        } catch (error) {
            console.error("Error adding pilot:", error);
        }
    }


    async function deletePilot(id: number) {
        const response = await fetch(`${apiUrl}/pilot/${id}`, {
            method: "DELETE",
        });
        if (response.ok) {
            piloti = piloti.filter((pilot) => pilot.idPilot !== id);
            console.log("Izbrisano letalo:", id);
        } else {
            console.error("Letalo ni bilo uspešno izbrisano:", response.statusText);
        }
    }

    onMount(() => {
        console.log(piloti)
      getPilots();
    });

    function refreshPage() {
        getPilots();
    }

  </script>
  
  <main class=" flex flex-col gap-6 max-w-7xl mx-auto px-4 py-8">
    <section>
      <h1 class="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl mb-8 text-center text-gray-800">
        Piloti
      </h1>
    </section>

    <!-- <section>
      <Carousel.Root>
        <Carousel.Content class="flex gap-4">       
          {#each piloti as pilot}
            <Carousel.Item class="carousel-item">
              <div class="plane-card w-full max-w-7xl mx-auto p-6 rounded-lg border-solid border-2 border-indigo-500 shadow-md bg-white transition-transform duration-300 hover:scale-105 hover:shadow-lg">
                <h2 class="text-2xl font-semibold text-gray-800 mb-2">{pilot.idPilot}</h2>
                <p class="text-gray-600"><strong>Ime:</strong> {pilot.ime}</p>
                <p class="text-gray-600"><strong>Priimek:</strong> {pilot.priimek}</p>
                <Button class="bg-red-500 text-white" on:click={() => deletePilot(pilot.idPilot)}>Izbrisi pilota</Button>
              </div>
            </Carousel.Item>
          {/each}
        </Carousel.Content>
        <Carousel.Previous class="carousel-control" />
        <Carousel.Next class="carousel-control" />
      </Carousel.Root>
    </section>
 -->
    <section>
      <Table.Root>
          <Table.Header>
              <Table.Row class="table-row">
                  <Table.Head>ID</Table.Head>
                  <Table.Head>Ime</Table.Head>
                  <Table.Head>Priimek</Table.Head>
                  <Table.Head></Table.Head>
              </Table.Row>
          </Table.Header>
          <Table.Body>

            <Table.Row>
            
<Table.Cell></Table.Cell>
<Table.Cell>
    <input 
        type="text" 
        class="block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" 
        bind:value={newPilot.ime} 
        placeholder="Ime" 
    />
</Table.Cell>
<Table.Cell>
    <input 
        type="text" 
        class="block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" 
        bind:value={newPilot.priimek} 
        placeholder="Priimek" 
    />
</Table.Cell>
<Table.Cell>
    <Button class="bg-green-500 text-white px-4 py-2 rounded-md shadow hover:bg-green-600" on:click={addPilot}>Dodaj Pilota</Button>
</Table.Cell>
            </Table.Row>
              {#each piloti as pilot}
                  <Table.Row>
                      <Table.Cell>{pilot.idPilot}</Table.Cell>
                      <Table.Cell>{pilot.ime}</Table.Cell>
                      <Table.Cell>{pilot.priimek}</Table.Cell>
                      <Table.Cell><Button class="bg-red-500 text-white" on:click={() => deletePilot(pilot.idPilot)}>Izbrisi Pilota</Button></Table.Cell>
                  </Table.Row>
              {/each}
          </Table.Body>
      </Table.Root>
  </section>
  </main>
  
  <style>
    .carousel-item {
      display: flex;
      justify-content: center;
      width: 100%;
      padding: 1rem;
    }
  
    .plane-card {
      width: 100%;
      background: white;
      border-radius: 0.75rem;
      padding: 1.5rem;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      transition: transform 0.3s, box-shadow 0.3s;
    }
  
    .plane-card:hover {
      transform: scale(1.02);
      box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
    }
  
    .plane-card h2 {
      color: #2d3748;
    }
  
    .plane-card p {
      color: #4a5568;
      margin-bottom: 0.5rem;
    }
  
    .carousel-control {
      font-size: 1.5rem;
      color: #4a5568;
      background: transparent;
      border: none;
      cursor: pointer;
      transition: color 0.3s;
    }
  
    .carousel-control:hover {
      color: #2d3748;
    }
  </style>
  
  
  
  