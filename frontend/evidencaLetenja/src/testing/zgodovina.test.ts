import { render, screen, fireEvent, waitFor } from '@testing-library/svelte';
import Page from '/home/benjamin/Desktop/RIRSProjekt/RIRS_EvidencaLetenjaProjekt/frontend/evidencaLetenja/src/routes/zgodovina/+page.svelte';
import { describe, it, expect, vi, type Mock } from 'vitest';
import '@testing-library/jest-dom';

// Mock the API calls
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
    (fetch as Mock).mockResolvedValue({
      ok: true,
      json: async () => mockPoleti,
    });
  });

  it('renders "Zgodovina letov" text', async () => {
    render(Page);

    // Check if the text "Zgodovina letov" is present
    expect(screen.getByText('Zgodovina letov')).toBeInTheDocument();
  });

  it('renders table rows with flight data', async () => {
    render(Page);

    await waitFor(() => screen.getByText('ID'));

    expect(screen.getByText('123')).toBeInTheDocument();
    expect(screen.getByText('456')).toBeInTheDocument();
    
  });

  it('simulates clicking the "Delete" button', async () => {
    render(Page);

    // Wait for the table to render
    await waitFor(() => screen.getByText('Zgodovina letov'));

    const deleteButtons = screen.getAllByText('Delete');
    expect(deleteButtons.length).toBe(2); 

    // Mock the delete function (you can spy on the method if it's passed as a prop)
    const mockDelete = vi.fn();

    // Since deleteFlight is an async function, you need to ensure the signature matches
    render(Page, {
      props: {
        deleteFlight: mockDelete, // Inject the mock function
      },
    });

    // Simulate a click on the delete button for the first row
    await fireEvent.click(deleteButtons[0]);

    // Check that deleteFlight function was called with the correct argument (flight ID)
    expect(mockDelete).toHaveBeenCalledWith(1);
  });

  it('checks the content of a specific row and simulates interaction', async () => {
    render(Page);

    // Wait for the table to render
    await waitFor(() => screen.getByText('Zgodovina letov'));

    // Check if specific flight data is rendered correctly
    const firstRow = screen.getByText('1').closest('tr');
    expect(firstRow).toBeInTheDocument();

    // Check if the correct pilot ID is rendered for the first flight
    expect(firstRow?.textContent).toContain('123');

    // Optionally, simulate clicking the edit button (if available in your setup)
    const editButton = screen.getByText('Uredi');
    expect(editButton).toBeInTheDocument();

    // Simulate click on the 'Edit' button (assuming there's an 'Edit' button in the dialog)
    await fireEvent.click(editButton);

    // Verify that the modal/dialog shows the correct initial data
    const pilotInput = screen.getByLabelText('Pilot ID');
    expect(pilotInput.value).toBe('123');  // Assuming Pilot ID is the field you want to check
  });
});
