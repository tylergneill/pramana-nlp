<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="//div/p">
<p>
<xsl:copy-of select="./@*"/>

<xsl:variable name="curr_page" select="@page"/>

<xsl:attribute name="page2">
<xsl:value-of select="count(preceding-sibling::p[@page=$curr_page])+1"/>
</xsl:attribute>

<xsl:copy-of select="./node()"/>
</p>
</xsl:template>

<xsl:template match="pb" />

</xsl:stylesheet>