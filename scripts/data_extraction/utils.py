from bs4 import BeautifulSoup
import sys
import os
import re
reload(sys)
sys.setdefaultencoding('UTF8')

def get_blurb(soup):
	blurb = soup.find('div', class_ = "short_blurb")
	if blurb is not None:
		return blurb.get_text().replace('\n\n', '\n')
	else:
		return ''

def get_full_description(soup):
	description = soup.find('div', class_="full-description")
	if description is not None:
		return description.get_text().replace('\n\n', '\n')
	else:
		return ''


def get_risks(soup):
	risks = soup.find('div', id="risks")
	if risks is None:
		risks = soup.findAll('div', class_ = "mb6")
		for risk in risks:
			if 'Risks and challenges' in risk.get_text():
				return risk.get_text().replace('\n\n', '\n').replace('Risks and challenges', '').replace('Learn about accountability on Kickstarter', '')
		return ''	
	else:
		return risks.get_text().replace('\n\n', '\n').replace('Risks and challenges', '').replace('Learn about accountability on Kickstarter', '')


def get_rewards(soup):
	#Where all the rewards are
	reward_section = soup.find_all('div', class_="NS_backer_rewards__reward p2")
	
	#Match numbers
	pattern = re.compile(r'[^0-9]')

	#Getting the reward amounts
	reward_currency = ''
	reward_amount_sections = []
	reward_item_sections = []
	reward_amounts = []
	reward_items = []
	for reward_item in reward_section:
		reward_amount_sections.append(reward_item.find_all("h5", class_="mb1"))
		reward_item_sections.append(reward_item.find_all("div", class_="mb2"))
			
	for reward_amount in reward_amount_sections:
		reward_amounts.append(int(pattern.sub('', unicode(reward_amount).split('>')[2].split("</span")[0])))
		reward_currency = unicode(reward_amount).split("money ")[1].split()[0]

	for reward_item in reward_item_sections:
		reward_items.append(unicode(reward_item).split('>')[2].split("</p")[0].strip())

	rewards_and_amounts = []
	
	#reward_amounts_numbers has the reward amounts
	if len(reward_amounts) != len(reward_items):
		return []
	else:
		for i in range(len(reward_amounts)):
			rewards_and_amounts.append([int(reward_amounts[i]), reward_items[i]])
			
	return reward_currency, rewards_and_amounts
	
