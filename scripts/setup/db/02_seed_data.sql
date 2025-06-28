-- DML: Seed data for Hotel Management Toolbox

-- Insert hotel tiers
INSERT INTO hotel_tier (tier_name, cost) VALUES
('Luxury', 100),
('Upper Upscale', 50),
('Upscale', 40),
('Upper Midscale', 30),
('Midscale', 20),
('Budget', 10)
ON CONFLICT DO NOTHING;

-- Insert hotels
INSERT INTO hotels(id, name, location, hotel_tier_id) VALUES 
(1, 'Hilton Basel', 'Basel', 1),
(2, 'Marriott Zurich', 'Zurich', 3),
(3, 'Hyatt Regency Basel', 'Basel', 2),
(4, 'Radisson Blu Lucerne', 'Lucerne', 5),
(5, 'Best Western Bern', 'Bern', 4),
(6, 'InterContinental Geneva', 'Geneva', 1),
(7, 'Sheraton Zurich', 'Zurich', 2),
(8, 'Holiday Inn Basel', 'Basel', 4),
(9, 'Courtyard Zurich', 'Zurich', 3),
(10, 'Comfort Inn Bern', 'Bern', 5)
ON CONFLICT (id) DO NOTHING;

-- Insert sample bookings
INSERT INTO bookings (hotel_id, checkin_date, checkout_date)
VALUES
  (1, '2025-07-01', '2025-07-05'),
  (2, '2025-07-10', '2025-07-12'),
  (3, '2025-08-15', '2025-08-20'),
  (4, '2025-09-01', '2025-09-03'),
  (5, '2025-09-10', '2025-09-15'); 