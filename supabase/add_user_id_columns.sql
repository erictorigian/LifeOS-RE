-- Add user_id columns to CRM tables
-- Run this in your Supabase SQL editor

-- Add user_id to crm_contacts
ALTER TABLE public.crm_contacts 
ADD COLUMN IF NOT EXISTS user_id UUID DEFAULT '00000000-0000-0000-0000-000000000000';

-- Add user_id to crm_deals
ALTER TABLE public.crm_deals 
ADD COLUMN IF NOT EXISTS user_id UUID DEFAULT '00000000-0000-0000-0000-000000000000';

-- Add user_id to crm_interactions
ALTER TABLE public.crm_interactions 
ADD COLUMN IF NOT EXISTS user_id UUID DEFAULT '00000000-0000-0000-0000-000000000000';

-- Add user_id to crm_next_actions
ALTER TABLE public.crm_next_actions 
ADD COLUMN IF NOT EXISTS user_id UUID DEFAULT '00000000-0000-0000-0000-000000000000';

-- Update existing rows with your user_id (optional - only if you want to set existing data)
-- UPDATE public.crm_contacts SET user_id = '11111111-1111-1111-1111-111111111111' WHERE user_id = '00000000-0000-0000-0000-000000000000';
-- UPDATE public.crm_deals SET user_id = '11111111-1111-1111-1111-111111111111' WHERE user_id = '00000000-0000-0000-0000-000000000000';
-- UPDATE public.crm_interactions SET user_id = '11111111-1111-1111-1111-111111111111' WHERE user_id = '00000000-0000-0000-0000-000000000000';
-- UPDATE public.crm_next_actions SET user_id = '11111111-1111-1111-1111-111111111111' WHERE user_id = '00000000-0000-0000-0000-000000000000';

