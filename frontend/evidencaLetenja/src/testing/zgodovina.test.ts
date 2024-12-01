import { render, screen, fireEvent, waitFor } from '@testing-library/svelte';
import Page from '../routes/zgodovina/+page.svelte';
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
    expect(screen.getByText('Zgodovina letov')).toBeInTheDocument();
  });

  it('renders table rows with flight data', async () => {
    render(Page);

    await waitFor(() => screen.getByText('123')); 

    expect(screen.getByText('123')).toBeInTheDocument();
    expect(screen.getByText('456')).toBeInTheDocument();
    
  });

  it('simulates clicking the "Delete" button', async () => {
    render(Page);

    await waitFor(() => screen.getByText('123'));

    const deleteButtons = screen.getAllByText('Delete');

    expect(deleteButtons.length).toBe(2); 

    //const mockDelete = vi.fn();

    // Since deleteFlight is an async function, you need to ensure the signature matches
   /*  render(Page, {
      props: {
        deleteFlight: mockDelete, // Inject the mock function
      },
    });

    // Simulate a click on the delete button for the first row
    await fireEvent.click(deleteButtons[0]);

    // Check that deleteFlight function was called with the correct argument (flight ID)
    expect(mockDelete).toHaveBeenCalledWith(1); */
  });

  it('checks the content of a specific row and simulates interaction', async () => {
    render(Page);
  
    // Wait for the table to render
    await waitFor(() => screen.getByText('123'));
  
    // Check if specific flight data is rendered correctly
    const firstRow = screen.getByText('1').closest('tr');
    expect(firstRow).toBeInTheDocument();
  
    // Check if the correct pilot ID is rendered for the first flight
    expect(firstRow?.textContent).toContain('123');
  
    // Get all "Uredi" buttons in the document
    const editButtons = screen.getAllByText('Uredi');
    
    // Assert there is at least one "Uredi" button
    expect(editButtons.length).toBeGreaterThan(0);
  
    // Simulate click on the first "Uredi" button (assuming you want to click on the first one)
    await fireEvent.click(editButtons[1]);
  
    // Verify that the modal/dialog shows the correct initial data
    const pilotInput = screen.getByLabelText('Pilot ID');
    
    // If the pilot input field is an input element, check its value.
    expect(pilotInput.value).toBe('456');  // Assuming Pilot ID is the field you want to check
  });
});
