import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import fetchMock from 'jest-fetch-mock';

// Mock the blocks.js file
jest.mock('../public/blocks.js');

describe('Repository Manager', () => {
  beforeEach(() => {
    fetchMock.resetMocks();
  });

  test('fetches and displays organizations', async () => {
    const mockOrgs = [{ id: 1, name: 'Org1' }, { id: 2, name: 'Org2' }];
    fetchMock.mockResponseOnce(JSON.stringify({ organizations: mockOrgs }));

    render(<div id="app" />);
    
    await waitFor(() => {
      expect(screen.getByText('Org1')).toBeInTheDocument();
      expect(screen.getByText('Org2')).toBeInTheDocument();
    });
  });

  test('fetches and displays repositories for selected organization', async () => {
    const mockRepos = [{ id: 1, name: 'Repo1', html_url: 'https://github.com/Org1/Repo1' }];
    fetchMock.mockResponseOnce(JSON.stringify(mockRepos));

    render(<div id="app" />);
    
    const select = screen.getByRole('combobox');
    fireEvent.change(select, { target: { value: 'Org1' } });

    await waitFor(() => {
      expect(screen.getByText('Repo1')).toBeInTheDocument();
    });
  });

  test('removes repository when remove button is clicked', async () => {
    fetchMock.mockResponseOnce(JSON.stringify({ success: true }));

    render(<div id="app" />);
    
    const removeButton = screen.getByText('[-]');
    fireEvent.click(removeButton);

    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledWith(
        expect.stringContaining('/api/remove-repository'),
        expect.objectContaining({ method: 'POST' })
      );
    });
  });
});
