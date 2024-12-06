<script lang="ts">
  import * as Dialog from "$lib/components/ui/dialog/index.js";
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input/index.js";
  import { Label } from "$lib/components/ui/label/index.js";

  export let pilot: {
    idPilot: number;
    ime: string;
    priimek: string;
  };

  let isDialogOpen = false;

  export let onSave: (pilotData: {
    ime: string;
    priimek: string;
  }) => void;

  async function handleSave() {
    const pilotData = {
      ime: pilot.ime,
      priimek: pilot.priimek,
    };

    console.log(pilotData);
    onSave(pilotData);
    isDialogOpen = false;
  }
</script>

<Dialog.Root bind:open={isDialogOpen}>
  <Dialog.Trigger
    class="mt-6 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
  >
    Dodaj
  </Dialog.Trigger>
  <Dialog.Content class="sm:max-w-[425px]">
    <Dialog.Header>
      <Dialog.Title>Dodaj pilota</Dialog.Title>
      <Dialog.Description>Tukaj lahko dodate novega pilota</Dialog.Description>
    </Dialog.Header>
    <div class="grid grid-cols-4 items-center gap-4">
      <Label for="cas_vzleta" class="text-right">Ime</Label>
      <Input bind:value={pilot.ime} id="ime" class="col-span-3" />
    </div>
    <div class="grid grid-cols-4 items-center gap-4">
      <Label for="cas_vzleta" class="text-right">Priimek</Label>
      <Input bind:value={pilot.priimek} id="ime" class="col-span-3" />
    </div>
    <Dialog.Footer>
      <Button on:click={handleSave}>Shrani</Button>
    </Dialog.Footer>
  </Dialog.Content>
</Dialog.Root>
