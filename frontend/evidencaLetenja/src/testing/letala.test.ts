import { render, screen, fireEvent, waitFor } from '@testing-library/svelte';
import { describe, it, expect, vi } from 'vitest';
import Page from '../routes/zgodovina/+page.svelte';
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

// Mock the fetch API
global.fetch = vi.fn();

describe('Page Component', () => {
  const mockPoleti = [
    {
      idPolet: 1,
      cas_vzleta: '01/02/2002 10:00',
      cas_pristanka: '01/02/2002 12:00',
      Pilot_idPilot: 123,
    },
    {
      idPolet: 2,
      cas_vzleta: '02/03/2003 14:00',
      cas_pristanka: '02/03/2003 16:00',
      Pilot_idPilot: 456,
    },
  ];

  beforeEach(() => {
    (fetch as vi.Mock).mockResolvedValue({
      ok: true,
      json: async () => mockPoleti,
    });
  });

  it('renders "Zgodovina letov" text', async () => {
    render(Page);
    expect(screen.getByText('Zgodovina letov')).toBeInTheDocument();
  });

  it('renders table rows with flight data', async () => {
    render(Page);

    await waitFor(() => screen.getByText('123')); // Wait for data to load

    expect(screen.getByText('123')).toBeInTheDocument();
    expect(screen.getByText('456')).toBeInTheDocument();
  });

  it('simulates clicking the "Delete" button', async () => {
    render(Page);

    await waitFor(() => screen.getByText('123'));

    const deleteButtons = screen.getAllByText('Delete');
    expect(deleteButtons.length).toBe(2); // Check if delete buttons are present
  });

  it('checks the content of a specific row and simulates interaction', async () => {
    render(Page);

    await waitFor(() => screen.getByText('123')); // Wait for data to load

    // Check if specific flight data is rendered correctly
    const firstRow = screen.getByText('1').closest('tr');
    expect(firstRow).toBeInTheDocument();

    // Check if the correct pilot ID is rendered for the first flight
    expect(firstRow?.textContent).toContain('123');

    // Get all "Uredi" buttons in the document
    const editButtons = screen.getAllByText('Uredi');
    expect(editButtons.length).toBeGreaterThan(0);

    // Simulate click on the first "Uredi" button (assuming you want to click on the first one)
    await fireEvent.click(editButtons[1]);

    // Verify that the modal/dialog shows the correct initial data
    const pilotInput = screen.getByLabelText('Pilot ID');
    expect(pilotInput.value).toBe('456');  // Assuming Pilot ID is the field you want to check
  });
});
