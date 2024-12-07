import { render, screen, fireEvent, waitFor } from '@testing-library/svelte';
import { describe, it, expect, vi } from 'vitest';
import Page from '../routes/piloti/+page.svelte'; // Replace with the actual path to your Svelte page/component
import '@testing-library/jest-dom';

// Mock EmblaCarousel import
vi.mock('embla-carousel-svelte', () => ({
  default: () => {
    return {
      // Mocking EmblaCarousel functions, no-op implementation
      init: vi.fn(),
      scrollTo: vi.fn(),
    };
  },
}));

global.fetch = vi.fn();

describe('Pilot Management Page', () => {
  const mockPilots = [
    { idPilot: 1, ime: 'Janez', priimek: 'Novak' },
    { idPilot: 2, ime: 'Ana', priimek: 'Kovač' },
  ];

  beforeEach(() => {
    (fetch as vi.Mock).mockResolvedValue({
      ok: true,
      json: async () => mockPilots,
    });
  });

  it('renders "Piloti" heading', async () => {
    render(Page);
    expect(screen.getByText('Piloti')).toBeInTheDocument();
  });

  it('renders table rows with pilot data', async () => {
    render(Page);

    await waitFor(() => screen.getByText('Ana')); 

    expect(screen.getByText('Ana')).toBeInTheDocument();
  });

  it('simulates clicking the "Delete" button', async () => {
    render(Page);

    await waitFor(() => screen.getByText('Ana'));

    const deleteButtons = screen.getAllByText('Izbrisi Pilota');
    expect(deleteButtons.length).toBe(2); 

  });

  it('checks the input fields and adds a new pilot', async () => {
    render(Page);

    const nameInput = screen.getByPlaceholderText('Ime');
    const surnameInput = screen.getByPlaceholderText('Priimek');
    const addButton = screen.getByText('Dodaj Pilota');

    await fireEvent.input(nameInput, { target: { value: 'Marko' } });
    await fireEvent.input(surnameInput, { target: { value: 'Pavlić' } });
    await fireEvent.click(addButton);

    expect(fetch).toHaveBeenCalledWith('http://localhost:8000/dodajPilota', expect.objectContaining({
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ idPilot: 0, ime: 'Marko', priimek: 'Pavlić' }),
    }));
  });

  it('removes a pilot from the table when "Delete" is clicked', async () => {
    render(Page);
  
    await waitFor(() => screen.getByText('Ana')); 
  
    let deleteButtons = screen.getAllByText('Izbrisi Pilota');
    expect(deleteButtons.length).toBe(2); 
  
    await fireEvent.click(deleteButtons[0]);

     deleteButtons = screen.getAllByText('Izbrisi Pilota');
    expect(deleteButtons.length).toBe(1);
  });
  

});
