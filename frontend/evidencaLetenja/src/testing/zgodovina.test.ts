import { render, screen, fireEvent, waitFor } from '@testing-library/svelte';
import Page from '../routes/zgodovina/+page.svelte';
import { describe, it, expect, vi, type Mock } from 'vitest';
import '@testing-library/jest-dom';


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

  it('remdera pravilno stran', async () => {
    render(Page);
    expect(screen.getByText('Zgodovina letov')).toBeInTheDocument();
  });

  it('rendera tabelo z leti', async () => {
    render(Page);

    await waitFor(() => screen.getByText('123')); 

    expect(screen.getByText('123')).toBeInTheDocument();
    expect(screen.getByText('456')).toBeInTheDocument();
    
  });

  it('preveri stevilo gumbov za brisanje', async () => {
    render(Page);

    await waitFor(() => screen.getByText('123'));

    const deleteButtons = screen.getAllByText('Delete');

    expect(deleteButtons.length).toBe(2); 

  });

  it('rendera stran ter preveri, če se modalno okno odpre', async () => {
    render(Page);
  
    await waitFor(() => screen.getByText('123'));
  
    const firstRow = screen.getByText('1').closest('tr');
    expect(firstRow).toBeInTheDocument();
  
    expect(firstRow?.textContent).toContain('123');
  
    const editButtons = screen.getAllByText('Uredi');
    
    expect(editButtons.length).toBeGreaterThan(0);
  
    await fireEvent.click(editButtons[1]);
  
    const pilotInput = screen.getByLabelText('Pilot ID');
    
    expect(pilotInput.value).toBe('456');  

  });
});
