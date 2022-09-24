This project is the Case Study project for QuickCheck
What I need
- A simple html page
  - Implement a view to list the latest news;
  - Allow filtering by the type of item;
  - Implement a search box for filtering by text;
  - As there are hundreds of news you probably want to use pagination or lazy loading when you display them.
- Backend
- Make a scheduled job to sync the published news to a DB every 5 minutes. You can start with the latest 100 items, and sync every new item from there. Note: here are several types of news (items), with relations between them; 
- Cron Job
- Expose /api route to update data
- Database